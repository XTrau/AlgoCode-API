## Dev

Run postgres database in docker

```
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres
```

Run Redis (broker for Celery) in docker

```
docker run -d -p 6379:6379 redis redis-server --requirepass redis
```

Run Backend

```
python src/main.py
```

Run Celery

```
celery -A src.worker.celery_app worker --loglevel=info --pool=solo
```

## Create ssl keys for auth working

```
mkdir certs 
cd certs
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in private_key.pem -out public_key.pem
cd ..
```

## Create folder for upload files

```
mkdir uploads
```
