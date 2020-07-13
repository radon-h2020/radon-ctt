FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN apk --update add python3 py3-pip openssl ca-certificates py3-openssl wget git aws-cli
RUN apk --update add --virtual local-deployment-docker docker docker-compose docker-py
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python3-dev build-base \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies

COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "openapi_server"]
