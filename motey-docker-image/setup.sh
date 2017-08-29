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

cd /opt
git clone https://github.com/Neoklosch/Motey.git

cd /opt/Motey/

python3 setup.py build
python3 setup.py install

cd /opt/Motey/webclient/
curl -sL https://deb.nodesource.com/setup_8.x | bash -
apt-get install -y nodejs
npm install http-server -g
