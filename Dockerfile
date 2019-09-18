FROM python:3-alpine
LABEL maintainer="Andrey Andreev <andyceo@yandex.ru> (@andyceo)"
ENV PIP_REQUIRED_PACKAGES "influxdb pymongo requests"
ENV PIP_SUGGESTED_PACKAGES "python-dateutil tabulate"
RUN apk add --update --no-cache ca-certificates && \
    pip --no-cache-dir --disable-pip-version-check install `echo " $PIP_REQUIRED_PACKAGES"` && \
    pip --no-cache-dir --disable-pip-version-check install `echo " $PIP_SUGGESTED_PACKAGES"` && \
    rm -rf /tmp/* /var/tmp/*
COPY .  /app/pylibs
WORKDIR /app
