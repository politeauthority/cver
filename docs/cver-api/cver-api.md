# Cver Api

## Install
### Mysql
@ToDo: Tighten up permissions
```sql
CREATE USER 'cver'@'%' IDENTIFIED BY '6XsSTirsXQ3wzGme9Z9Z';
ALTER USER 'cver'@'%' IDENTIFIED WITH mysql_native_password BY '6XsSTirsXQ3wzGme9Z9Z';
GRANT ALL PRIVILEGEs ON * . * TO 'cver'@'%';
```
### Secrets
Note: This will require a docker registry secret to pull private images!

```bash
kubectl create secret docker-registry regcred \
    --docker-server=harbor.squid-ink.us \
    --docker-username=politeauthority \
    --docker-password=password
```
You will need to create the secret `cver-secrets-prod`
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: cver-secrets-prod
data:
  mysql-password: NlhzU1RpcnNYUTN3ekdtZTlaOVo=
  cver-secret-key: ZGZ4MyZNZUAmQTM5
type: Opaque
```



### Helm


```bash
helm upgrade --install \
    cver-api-prod \
    helm/cver-api \
    -f helm/cver-api/values-quigley-prod.yaml
```

## Api Usage

### Authentication
**POST** /auth
Headers
    client-id
    x-api-key
Returns a JWT
```
{
    "message": "",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJpYXQiOjE2ODUxMzU4NTcsImV4cCI6MTY4NTEzOTQ1N30.rgbN8P_nKd76ggKpAagos3pUeRZFHSlthIF41uOX9Fw"
}
```


Routes

/
/info
/debug
/auth
/api-key
/api-keys
/app
/apps
/image
/images
/image-build
/image-builds
/migrations
/options
/perm
/perms
/role
/roles
/role-perm
/role-perms
/user
/users
/submit-report
