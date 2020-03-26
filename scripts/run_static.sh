docker stop alcohall-static
docker container rm alcohall-static
docker image rm alcohall-static


docker build -t alcohall-static -f docker/static.Dockerfile .
docker run -itd --name alcohall-static -p 3000:80  alcohall-static