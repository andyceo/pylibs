#!/usr/bin/env bash
set -xe
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd $DIR
REV=$(git rev-parse --short=7 HEAD)
REPO=${REPO:-andyceo/pylibs}
TAG=${TAG:-revision-$REV}
sudo docker build -t $REPO:$TAG .
sudo docker push $REPO:$TAG
popd
