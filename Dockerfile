FROM python:3
LABEL maintainer=793746995@qq.com

WORKDIR /usr/app

COPY ./ .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8099

CMD ["sh", "docker_start.sh"]


