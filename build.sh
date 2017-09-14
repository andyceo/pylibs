#!/usr/bin/env bash
set -xe
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd $DIR
REV=$(git rev-parse --short=7 HEAD)
TAG=192.168.2.240:5000/pylibs:rev_$REV
sudo docker build -t $TAG .
sudo docker push $TAG
popd
