# Getting Started
The best way to install Cver is with helm. The helm package includes a Mysql distribution with it, however you can bring your own as well.
## Install
### Helm
You'll want to create your own `values.yaml` file. I've included a few examples of values file I use over at [helm/cver-api/](helm/cver-api)
```bash
cd cver/helm/cver-api
helm upgrade --install \
    cver-api-prod \
    helm/cver-api \
    -f helm/cver-api/values-quigley-prod.yaml
```
### Mysql
Once your service is up, log into Mysql and create a user
@note: This process will be automated eventually.
@ToDo: Tighten up permissions
```sql
CREATE USER 'cver'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGEs ON * . * TO 'cver'@'%';
```
