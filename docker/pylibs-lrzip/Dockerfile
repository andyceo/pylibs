FROM andyceo/pylibs
MAINTAINER Andrey Andreev <andyceo@yandex.ru> (@andyceo)
ENV LRZIP_BUILD_PACKAGES "git autoconf automake libtool gcc musl-dev zlib-dev bzip2-dev lzo-dev coreutils make g++"
ENV LRZIP_RUNTIME_PACKAGES "lzo libbz2 libstdc++"
ENV PYTHON_LRZIP_BUILD_PACKAGES "gcc libffi-dev musl-dev"

RUN echo "Build lrzip" && \
    apk add --update --no-cache `echo $LRZIP_BUILD_PACKAGES` && \
    git clone https://github.com/ckolivas/lrzip.git && \
    cd /app/lrzip && ./autogen.sh && ./configure && make -j `nproc` && make install && \
    echo "Install lrzip with pip" && \
    apk add --update --no-cache `echo $PYTHON_LRZIP_BUILD_PACKAGES` && \
    pip --no-cache-dir --disable-pip-version-check install \
        --global-option=build_ext --global-option="-I/app/lrzip" lrzip && \
    echo "Add runtime packages and cleanup" && \
    apk del --purge `echo $LRZIP_BUILD_PACKAGES $PYTHON_LRZIP_BUILD_PACKAGES` && \
    apk add --update --no-cache `echo $LRZIP_RUNTIME_PACKAGES` && \
    rm -rf /tmp/* /var/tmp/* /app/lrzip
