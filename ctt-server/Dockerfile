FROM python:3-alpine

ENV OPERA_SSH_HOST_KEY_CHECKING=False
ENV ANSIBLE_HOST_KEY_CHECKING=False

RUN echo -e "search home\nnameserver 8.8.8.8" > /etc/resolv.conf

ENV CLOUD_SDK_VERSION=345.0.0
ENV PATH=/google-cloud-sdk/bin:$PATH
RUN wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    tar xzf google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    rm google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    ln -s /lib /lib64 && \
    gcloud components update && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud --version

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
COPY test-requirements.txt /usr/src/app/

RUN apk --update add python3 py3-pip openssl ca-certificates py3-openssl wget git openssh
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python3-dev build-base rust cargo
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r test-requirements.txt
RUN apk del build-dependencies

COPY . /usr/src/app

EXPOSE 18080
ENTRYPOINT ["python3"]
CMD ["-m", "openapi_server"]

