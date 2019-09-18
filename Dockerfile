FROM python:3-alpine
LABEL maintainer="Andrey Andreev <andyceo@yandex.ru> (@andyceo)"
ENV PIP_REQUIRED_PACKAGES "influxdb pymongo requests"
ENV PIP_SUGGESTED_PACKAGES "python-dateutil tabulate"
RUN apk add --update --no-cache ca-certificates && \
    pip --no-cache-dir --disable-pip-version-check install `echo " $PIP_REQUIRED_PACKAGES"` && \
    pip --no-cache-dir --disable-pip-version-check install `echo " $PIP_SUGGESTED_PACKAGES"` && \
    mkdir /app && rm -rf /tmp/* /var/tmp/*
COPY ./bitfinex /app/pylibs/bitfinex
COPY ./__init__.py /app/pylibs/__init__.py
COPY config/config.py /app/pylibs/config.py
COPY ./influxdb.py /app/pylibs/influxdb.py
COPY ./mongodb.py /app/pylibs/mongodb.py
COPY ./utils.py /app/pylibs/utils.py
WORKDIR /app
