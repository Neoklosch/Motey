#!/bin/sh

# build image
docker build -t neoklosch/fog_node_prototype .

# commit image
docker commit bbd42c2ce2a4 neoklosch/fog_node_prototype

# upload image
docker push neoklosch/fog_node_prototype

# start the container with shared folder
docker run -ti -v /home/neoklosch/latex-projects/fog_node_prototype:/opt/docker-stuff
