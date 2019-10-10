FROM python:3-alpine
LABEL maintainer="Andrey Andreev <andyceo@yandex.ru> (@andyceo)"
COPY . /app
WORKDIR /app
RUN apk add --update --no-cache ca-certificates docker && \
    pip --no-cache-dir --disable-pip-version-check install -r requirements.txt && \
    rm -rf /tmp/* /var/tmp/*
EXPOSE 8070
CMD ["/app/labels.py"]
