FROM python:3.6-alpine
ENV PIP_REQUIRED_PACKAGES "influxdb pymongo requests"
ENV PIP_SUGGESTED_PACKAGES "tabulate"
RUN pip --no-cache-dir --disable-pip-version-check install $PIP_REQURED_PACKAGES && \
    pip --no-cache-dir --disable-pip-version-check install $PIP_SUGGESTED_PACKAGES && \
    mkdir /app
COPY . /app/pylibs
RUN rm -rf /app/pylibs/{.git,.gitignore,Dockerfile,README.md,build.sh}
