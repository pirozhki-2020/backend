docker-compose stop alcohall-api
docker-compose stop alcohall-db
docker-compose stop alcohall-nginx

docker-compose build
docker compose up -d