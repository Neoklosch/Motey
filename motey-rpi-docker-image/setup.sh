#!/bin/sh

apt-get update
apt-get -y upgrade && apt-get install -y curl nano locate man build-essential libssl-dev libffi-dev python-dev aufs-tools cgroupfs-mount git apparmor wget
apt-get install -y --force-yes apt-transport-https
apt-get prune -y python3 python3-pip
curl -sSL get.docker.com | sh

cd /tmp
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
tar -zxvf Python-3.5.2.tgz
cd /tmp/Python-3.5.2
./configure
make
make install
python3 --version

pip3 install --upgrade pip
pip3 install -r /tmp/requirements.txt

cd /opt
git clone https://github.com/Neoklosch/Motey.git

cd /opt/Motey/

python3 setup.py build
python3 setup.py install
