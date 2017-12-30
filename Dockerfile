FROM python:3.6-alpine
ENV PIP_REQUIRED_PACKAGES "influxdb pymongo requests"
ENV PIP_SUGGESTED_PACKAGES "tabulate"
RUN apk add --update --no-cache ca-certificates && \
    pip --no-cache-dir --disable-pip-version-check install `echo " $PIP_REQUIRED_PACKAGES"` && \
    pip --no-cache-dir --disable-pip-version-check install `echo " $PIP_SUGGESTED_PACKAGES"` && \
    mkdir /app && rm -rf /tmp/* /var/tmp/*
COPY . /app/pylibs
RUN rm -rf /app/pylibs/{docker,.git,.gitignore,Dockerfile,README.md,build.sh}
WORKDIR /app
