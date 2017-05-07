#!/bin/sh

apt-get update
apt-get -y upgrade && apt-get install -y curl nano locate man python3 python3-pip build-essential libssl-dev libffi-dev python-dev aufs-tools cgroupfs-mount cgroup-lite git apparmor
apt-get install -y --force-yes apt-transport-https
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
echo "deb https://download.docker.com/linux/ubuntu xenial stable" >> /etc/apt/sources.list
apt-get update
apt-get install -y docker-ce

pip3 install --upgrade pip
pip3 install -r /tmp/requirements.txt
