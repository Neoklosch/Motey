#!/bin/sh

apt-get update
apt-get -y upgrade && apt-get install -y curl nano locate man python3 python3-pip build-essential libssl-dev libffi-dev python-dev aufs-tools cgroupfs-mount cgroup-lite git apparmor
apt-get install -y --force-yes apt-transport-https
curl -sSL get.docker.com | sh

pip3 install --upgrade pip
pip3 install -r /tmp/requirements.txt

cd /opt
git clone https://github.com/Neoklosch/Motey.git

cd /opt/Motey/

python3 setup.py build
python3 setup.py install
