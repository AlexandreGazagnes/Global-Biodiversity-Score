#! /bin/bash

# build docker image
# --progress=plain for showing progress bar
sudo docker build -f ./Dockerfile  -t gbs:latest .

# run docker image
# -d for detached mode
sudo docker run  -p 8501:8501 gbs:latest

# if needed to run bash inside container
# docker exec -it <container-name> /bin/bash