Clone the version-10 branch of this repo

```shell
git clone https://github.com/khulnasoft/ragapp.git -b version-10 && cd docker
```

Build the images

```shell
export DOCKER_REGISTRY_PREFIX=ragapp
docker build -t ${DOCKER_REGISTRY_PREFIX}/ragapp-socketio:v10 -f build/ragapp-socketio/Dockerfile .
docker build -t ${DOCKER_REGISTRY_PREFIX}/ragapp-nginx:v10 -f build/ragapp-nginx/Dockerfile .
docker build -t ${DOCKER_REGISTRY_PREFIX}/erpnext-nginx:v10 -f build/erpnext-nginx/Dockerfile .
docker build -t ${DOCKER_REGISTRY_PREFIX}/ragapp-worker:v10 -f build/ragapp-worker/Dockerfile .
docker build -t ${DOCKER_REGISTRY_PREFIX}/erpnext-worker:v10 -f build/erpnext-worker/Dockerfile .
```
