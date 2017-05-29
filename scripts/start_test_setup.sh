#!/bin/bash

docker stop motey_cluster_01 motey_cluster_02 motey_cluster_03 motey_cluster_mqtt_broker
docker rm motey_cluster_01 motey_cluster_02 motey_cluster_03 motey_cluster_mqtt_broker

docker network create --subnet=172.18.0.0/16 motey_cluster_network

screen -S motey_cluster

screen -S motey_cluster -x -X screen docker run --net motey_cluster_network --ip="172.18.0.3" -p 1883:1883 -p 9001:9001 -v config:/mqtt/config:ro --name motey_cluster_mqtt_broker toke/mosquitto &

screen -S motey_cluster -x -X screen docker run -ti --net motey_cluster_network --ip="172.18.0.10" -v /var/run/docker.sock:/var/run/docker.sock -p 5123:5023 -p 5190:5090 -p 5191:5091 --name motey_cluster_01 neoklosch/motey
screen -S motey_cluster -x -X screen docker run -ti --net motey_cluster_network --ip="172.18.0.11" -v /var/run/docker.sock:/var/run/docker.sock -p 5223:5023 -p 5290:5090 -p 5291:5091 --name motey_cluster_02 neoklosch/motey
screen -S motey_cluster -x -X screen docker run -ti --net motey_cluster_network --ip="172.18.0.12" -v /var/run/docker.sock:/var/run/docker.sock -p 5323:5023 -p 5390:5090 -p 5391:5091 --name motey_cluster_03 neoklosch/motey

screen -X caption always "%{rw} * | %H * $LOGNAME | %{bw}%c %D | %{-}%-Lw%{rw}%50>%{rW}%n%f* %t %{-}%+Lw%<"
