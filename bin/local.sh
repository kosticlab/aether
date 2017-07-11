#!/bin/bash

sudo apt-get update
sudo apt-get install awscli jq python --assume-yes
printf "'${1}'\n'${2}'\n'${3}'\n\n" | /usr/bin/aws configure
git clone git@github.com:kosticlab/aether.git
cd aether
cd bin
sudo chmod +x *.sh;cd ..
./bin/replica_node_init.sh '${4}' '${5}' '${6}' '${7}' '${8}' '${9}' 2> error.log &'
