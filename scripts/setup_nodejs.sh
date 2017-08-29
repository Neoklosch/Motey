#!/bin/bash

cd opt/Motey/webclient/
curl -sL https://deb.nodesource.com/setup_8.x | bash -
apt-get install -y nodejs
npm install http-server -g
http-server -p 4040
