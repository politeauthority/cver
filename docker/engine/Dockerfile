# Cver-Engine
# The workhorse running syncs and scans
#
ARG DOCKER_REGISTRY="docker.io/library"
FROM ${DOCKER_REGISTRY}/debian:stable-slim as base
ARG CVER_BUILD=""
ENV CVER_BUILD="${CVER_BUILD}"
ENV CVER_VERSION="0.0.0"
ENV CVER_ENV=""
RUN apt-get update
RUN apt-get install curl gpg -y
# Install pip
RUN apt install python3-pip -y


# Install Docker
RUN mkdir -m 0755 -p /etc/apt/keyrings && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

WORKDIR /app/cver

ADD src/ /app

# Install Cver
RUN pip install --upgrade pip --break-system-packages
RUN cd /app && pip install --break-system-packages -r /app/requirements.txt
RUN cd /app && pip install --break-system-packages .

# --- Tests Node ---
FROM base AS tests

# Dev-Build

# Cver Tests
ENV CVER_API_URL="http://localhost:80"
ADD tests/ /tests