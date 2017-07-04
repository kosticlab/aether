#!/bin/bash

az login --username $1 -p $2
az account set --subscription $3
azure group create --name $4 --location $5
az network public-ip create --name $6 --resource-group $4 --location $5 --allocation-method Static --dns-name $7
VnetPrefix="192.168.0.0/16"
SubnetPrefix="192.168.1.0/24"
az network vnet create --name $8 --resource-group $4 --location $5 --address-prefix $VnetPrefix --subnet-name $9 --subnet-prefix $SubnetPrefix
INTERNALIP="192.168.1.101"
az network nic create --name ${10} --resource-group $4 --location $5 --subnet $9 --vnet-name $8 --private-ip-address $INTERNALIP --public-ip-address $6
OsImage="UbuntuLTS"
Username=ubuntu
IP=$(az vm create --name ${11} --resource-group $4 --image $OsImage --location $5 --size $21 --nics testnic --admin-username $Username --storage-sku Standard_LRS | grep publicIpAddress | awk -F ":" '{print $2}' | sed 's/[",]//g')
az vm open-port --port 22 -g $4 -n ${11} --priority 1100
az vm open-port --port 13001 -g $4 -n ${11} --priority 800

check_connection()
{
  (exec 3<>/dev/tcp/$IP/22) &>/dev/null
  if [ $? -ne 0 ]
  then
    sleep 30
    check_connection
  fi
}

check_connection

ssh -o "StrictHostKeyChecking=no" ubuntu@$IP 'sudo apt-get update; sudo apt-get install awscli jq python --assume-yes; printf "'${12}'\n'${13}'\n'${14}'\n\n" | /usr/bin/aws configure;git clone git@github.com:kosticlab/aether.git;cd aether;cd bin;sudo chmod +x *.sh;cd ..;./bin/replica_node_init.sh '${15}' '${16}' '${17}' '${18}' '${19}' '${20}' 2> error.log &'
