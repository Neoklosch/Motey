#!/bin/bash

# build image
docker build -t neoklosch/motey .

# build image for raspberry pi
docker build -t neoklosch/motey-rpi .

# commit image
docker commit 788a449e4063 neoklosch/motey

# commit image for raspberry pi
docker commit 788a449e4063 neoklosch/motey-rpi

# upload image
docker push neoklosch/motey

# upload image for raspberry pi
docker push neoklosch/motey-rpi

# start the container with shared folder
docker run -ti -v /var/run/docker.sock:/var/run/docker.sock -v /home/neoklosch/projects/Motey:/opt/docker-stuff -p 5023:5023 -p 4200:4200 neoklosch/motey
docker run -ti -v /var/run/docker.sock:/var/run/docker.sock -v /home/neoklosch/projects/Motey:/opt/docker-stuff -p 5023:5023 -p 4200:4200 neoklosch/fog_node_prototype

# start mqtt server
docker run -p 1883:1883 -p 9001:9001 -v ./scripts/config:/mqtt/config:ro toke/mosquitto
