#!/bin/bash

# build image
docker build -t neoklosch/motey .

# commit image
docker commit 788a449e4063 neoklosch/motey

# upload image
docker push neoklosch/motey

# start the container with shared folder
docker run -ti -v /var/run/docker.sock:/var/run/docker.sock -v /home/neoklosch/projects/Motey:/opt/docker-stuff -p 5023:5023 neoklosch/motey

# start mqtt server
docker run -p 1883:1883 -p 9001:9001 -v ./scripts/config:/mqtt/config:ro toke/mosquitto
