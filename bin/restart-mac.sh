#!/bin/bash

# 检查操作系统类型
OS_NAME=$(uname -s)

# 根据操作系统选择合适的 ps 参数
case $OS_NAME in
    Linux)
        PS_CMD="ps -eux"
        ;;
    Darwin)
        PS_CMD="ps aux"  # macOS 使用 aux
        ;;
    *)
        echo "Unsupported operating system: $OS_NAME"
        exit 1
        ;;
esac

# 杀死 gunicorn 进程
$PS_CMD | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null
echo "Killed gunicorn processes"

# 杀死 celery 进程
$PS_CMD | grep celery | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null
echo "Killed celery processes"

# 获取当前脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Script directory: $SCRIPT_DIR"

# 切换到项目目录
if [ -d "$SCRIPT_DIR" ]; then
    cd "../$SCRIPT_DIR"
    echo "Changed to directory: $(pwd)"
else
    echo "Error: Cannot find project directory"
    exit 1
fi

# 收集静态文件
if [ -f "./venv/bin/python3" ]; then
    ./venv/bin/python3 manage.py collectstatic --noinput
    echo "Static files collected"
else
    echo "Warning: Python virtual environment not found or manage.py not found"
    # 尝试使用系统 python
    if command -v python3 &> /dev/null; then
        python3 manage.py collectstatic --noinput
    else
        echo "Error: Python3 not found"
    fi
fi

# 创建日志目录
mkdir -p logs

# 启动 celery worker
if [ -f "./venv/bin/celery" ]; then
    nohup ./venv/bin/celery -A django_exercise worker --loglevel=info > logs/celery_worker.log 2>&1 &
    echo "Celery worker started"
else
    echo "Error: Celery not found in virtual environment"
fi

# 启动 celery beat
if [ -f "./venv/bin/celery" ]; then
    nohup ./venv/bin/celery -A django_exercise beat --loglevel=info > logs/celery_beat.log 2>&1 &
    echo "Celery beat started"
fi

# 启动 gunicorn
if [ -f "./venv/bin/gunicorn" ]; then
    # 检查是否是 macOS
    if [ "$OS_NAME" = "Darwin" ]; then
        # macOS 不需要 BUILD_ID
        ./venv/bin/gunicorn django_exercise.wsgi:application -c gunicorn_config.py
    else
        # Linux 系统保留 BUILD_ID
        BUILD_ID=DONTKILLME ./venv/bin/gunicorn django_exercise.wsgi:application -c gunicorn_config.py
    fi
else
    echo "Error: Gunicorn not found in virtual environment"
    exit 1
fi