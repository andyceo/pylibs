FROM python:3-alpine
LABEL maintainer="Andrey Andreev <andyceo@yandex.ru> (@andyceo)"
ENV PIP_SUGGESTED_PACKAGES "deepmerge python-dateutil tabulate"
COPY .  /app/pylibs
WORKDIR /app
RUN apk add --update --no-cache ca-certificates && \
    pip --no-cache-dir --disable-pip-version-check install -r pylibs/requirements.txt && \
    pip --no-cache-dir --disable-pip-version-check install `echo " $PIP_SUGGESTED_PACKAGES"` && \
    rm -rf /tmp/* /var/tmp/*
