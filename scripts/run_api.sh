docker image rm alcohall
docker container rm alcohall

docker build -t alcohall .
docker run -itd --name alcohall -p 8000:8000 alcohall