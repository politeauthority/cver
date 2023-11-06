# Cver 0.0.4
![Regression Tests](https://github.com/politeauthority/cver/actions/workflows/push-stage.yaml/badge.svg)

Cver provides visability into container workloads, in realtime and historically. It allows you to
keep track of what images are in use, where they are being sourced from and the security risks they 
may pose to you.

## How it works
Cver is broken in 3 parts, the Cver Api, Cver Ingestion and Cver Engine.

### Cver Api
Cver Api provides the interface for all applications to write and read data from the Cver platform.

### Cver Ingest
Cver Ingest is the application which collects data from Kubernetes clusters, Docker hosts, or
anything else that wants to supply data from Cver to ingest.

### Cver Engine
Cver Engine runs all the back end operations of Cver. It manages downloading/ scaning container
images as well as pruning and organizing all the data Cver oversees.

[Getting Started](docs/getting-started.md)

[Cver Api](docs/cver-api/cver-api.md)

[Development](docs/development.md)
