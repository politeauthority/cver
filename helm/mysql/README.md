# Mysql
helm repo add bitnami https://charts.bitnami.com/bitnami


helm upgrade --install cver-mysql bitnami/mysql --set "auth.rootPassword=cleancut"


docker pull politeauthority/cver-api:f801e85936f5c161fc188b216e03ff2245f3065d