FROM python:3.11
LABEL maintainer=793746995@qq.com

ARG ENV=online
WORKDIR /usr/app

COPY ./ .
RUN mkdir -p /usr/app/logs
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ENV ENV ${ENV}
EXPOSE 8099

CMD ["sh", "docker_start.sh"]


