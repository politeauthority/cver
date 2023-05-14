# Cver-Api
# This container runs the Cver api web app
#

FROM python:3.10-alpine3.16

ENV CVER_DB_HOST="cver-mysql"
ENV CVER_DB_PORT="3306"
ENV CVER_DB_NAME="cver"
ENV CVER_DB_USER="user"
ENV CVER_DB_PASS=""
ENV CVER_VERSION="0.0.1"
ENV CVER_BUILD=""
ENV CVER_ENV=""

ADD scripts/entrypoint.sh /
ADD src/ /app
WORKDIR /app/cver

# Prod-Build Pignus-Api
RUN pip install --upgrade pip
RUN cd /app && pip install -r /app/requirements.txt
RUN cd /app && pip install .

CMD /entrypoint.sh

# Dev-Build
RUN apk add bash curl vim mysql-client
# Add Scripts
ADD scripts/cver-build /bin
ADD scripts/cver-run-api /bin
ADD scripts/cver-test-unit /bin
ADD scripts/cver-test-regression /bin
ADD scripts/cver-test-all /bin
ADD scripts/cver-db-login /bin

# Cver Tests
ENV CVER_API_URL="http://localhost:5001"
ENV CVER_DB_PASS=""
ADD tests/ /tests
