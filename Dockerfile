FROM python:3-alpine
LABEL maintainer="Andrey Andreev <andyceo@yandex.ru> (@andyceo)"
COPY .  /app/pylibs
WORKDIR /app
RUN apk add --update --no-cache ca-certificates && \
    pip --no-cache-dir --disable-pip-version-check install -r pylibs/requirements.txt && \
    rm -rf /tmp/* /var/tmp/*
