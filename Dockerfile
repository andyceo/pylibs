FROM python:3.6.2-alpine3.6

RUN pip --no-cache-dir --disable-pip-version-check install pymongo && \
    mkdir /app

COPY . /app/pylibs

RUN rm /app/pylibs/.git /app/pylibs/Dockerfile /app/pylibs/README.md
