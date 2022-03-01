FROM python:3
LABEL maintainer=793746995@qq.com

ARG ENV=online
WORKDIR /usr/app

COPY ./ .

RUN pip install --no-cache-dir -r requirements.txt
ENV ENV ${ENV}
EXPOSE 8099

CMD ["sh", "docker_start.sh"]


