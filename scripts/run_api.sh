docker stop alcohall-api
docker container rm alcohall-api
docker image rm alcohall-api


docker build -t alcohall-api -f docker/api.Dockerfile .
docker run -itd --name alcohall-api -p 10000:10000 alcohall-api