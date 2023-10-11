# Cver-Engine
# The work horse running syncs and scans
#
ARG DOCKER_REGISTRY="docker.io/library"
FROM ${DOCKER_REGISTRY}/python:3.10-slim as base
ARG CVER_BUILD=""
ENV CVER_BUILD="${CVER_BUILD}"
ENV CVER_VERSION="0.0.0"
ENV CVER_ENV=""
ENV TIMEOUT_SECONDS="300"
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

# Install trivy
RUN apt-get -y install wget apt-transport-https gnupg lsb-release
RUN wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add -
RUN echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | tee -a /etc/apt/sources.list.d/trivy.list
RUN apt-get update
RUN apt-get install -y trivy

WORKDIR /app/cver

ADD src/ /app
ADD scripts/entrypoint.sh /entrypoint.sh

# Install Cver
RUN pip install --upgrade pip --break-system-packages
RUN cd /app && pip install --break-system-packages -r /app/requirements.txt
RUN cd /app && pip install --break-system-packages .

CMD /entrypoint.sh

# --- Tests Node ---
FROM base AS tests
ENV PS1="cver-engine# "
ADD scripts/cver-build /bin
ADD scripts/cver-build-tests /bin
ADD tests/ /tests
# RUN cd /tests/ && python3 setup.py build && python3 setup.py install
# RUN pip install -r /tests/requirements.txt
