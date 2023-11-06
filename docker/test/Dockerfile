# Cver-Test
# This container runs all unit and regression tests for Cver
#
ARG DOCKER_REGISTRY="docker.io/library"
FROM ${DOCKER_REGISTRY}/python:3.10-alpine3.16 as base
ARG CVER_BUILD=""
ENV CVER_VERSION="0.0.0"
ENV GIT_CHECKOUT=""

# TEST vars
ENV CVER_TEST="false"
ENV CVER_CLIENT_ID=""
ENV CVER_API_KEY=""

WORKDIR /tests/
ADD requirements-src.txt /test/requirements-test.txt
ADD requirements-test.txt /test/requirements-src.txt

ADD scripts/cver-build /bin
ADD scripts/cver-test-unit /bin
ADD scripts/cver-test-flake8 /bin
ADD scripts/cver-cicd-regression /bin
ADD scripts/cver-cicd-unit /bin
ADD scripts/cver-db-destroy /bin

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers bash curl git vim \
    && apk add libffi-dev

ENV PS1="cver-test# "

RUN pip install -r /test/requirements-src.txt && \
    pip install -r /test/requirements-test.txt

# Cver Tests
ENV CVER_API_URL="http://localhost/"
ENV CVER_TEST_DIR="/tests/"
