#!/bin/sh

# build image
docker build -t neoklosch/fog_node_prototype .

# commit image
docker commit 788a449e4063 neoklosch/fog_node_prototype

# upload image
docker push neoklosch/fog_node_prototype

# start the container with shared folder
docker run -ti -v /var/run/docker.sock:/var/run/docker.sock -v /home/neoklosch/projects/fog_node_prototype:/opt/docker-stuff -p 5023:5023 neoklosch/fog_node_prototype

# start mqtt server
docker run -p 1883:1883 -p 9001:9001 -v ./scripts/config:/mqtt/config:ro toke/mosquitto
