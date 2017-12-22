FROM python:3.6-alpine
RUN pip --no-cache-dir --disable-pip-version-check install influxdb pymongo requests && mkdir /app
COPY . /app/pylibs
RUN rm -rf /app/pylibs/{.git,.gitignore,Dockerfile,README.md,build.sh}
