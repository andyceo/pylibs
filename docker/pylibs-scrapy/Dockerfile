FROM andyceo/pylibs
MAINTAINER Andrey Andreev <andyceo@yandex.ru> (@andyceo)
# Remove pillow and it's dependencies jpeg-dev, libjpeg-turbo if you do not want use image processing
ENV APK_DEVELOPMENT_PACKAGES "gcc jpeg-dev libffi-dev libxml2-dev libxslt-dev musl-dev openssl-dev zlib-dev"
RUN apk add --update --no-cache libjpeg-turbo libssl1.0 libxslt `echo $APK_DEVELOPMENT_PACKAGES` && \
    pip3 --no-cache-dir --disable-pip-version-check install pillow scrapy && \
    apk del `echo $APK_DEVELOPMENT_PACKAGES` && \
    rm -rf /tmp/* /var/tmp/*
