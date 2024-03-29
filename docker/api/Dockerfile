# Cver-Api
# This container runs the Cver api web app
#
ARG DOCKER_REGISTRY="docker.io/library"
FROM ${DOCKER_REGISTRY}/python:3.10-alpine3.16 as base
ARG CVER_BUILD=""
ENV CVER_VERSION="0.0.0"
ENV CVER_SECRET="secret"
ENV CVER_BUILD="${CVER_BUILD}"
ENV CVER_ENV=""
ENV CVER_DB_HOST="cver-mysql"
ENV CVER_DB_PORT="3306"
ENV CVER_DB_NAME="cver"
ENV CVER_DB_USER="user"
ENV CVER_DB_PASS=""

# TEST vars
ENV CVER_TEST="false"
ENV CVER_TEST_USER_CLIENT_ID=""
ENV CVER_TEST_USER_API_KEY=""

WORKDIR /app/cver

ADD scripts/entrypoint.sh /
ADD src/ /app

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev

# Install Cver
RUN pip install --upgrade pip 
RUN cd /app && pip install -r /app/requirements.txt
RUN cd /app && pip install .

CMD /entrypoint.sh

# --- Tests Node ---
FROM base AS dev

ENV PS1="cver-api# "
# Dev-Build
RUN apk add bash curl vim mysql-client
RUN pip install ipdb

# Add Scripts
ADD scripts/cver-api /bin
ADD scripts/cver-build /bin
ADD scripts/cver-run-api /bin
ADD scripts/cver-kill /bin
