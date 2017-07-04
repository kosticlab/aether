#!/bin/bash

#ARGS 1:sampletableloc 2:spinuptableloc 3:procs 4:mem 5:s3 folder to store output 6:aws login 7:aws password 8:azure login 9:azure password

#get instance ID
INSTANCE=$(cat /var/lib/cloud/data/instance-id)

#allocate elastic IP
/usr/bin/aws ec2 allocate-address --domain vpc > allocation.json

#get static IP and allocationID
IP=$(cat allocation.json | jq -r .PublicIp)
ALLOCATION=$(cat allocation.json | jq -r .AllocationId)
rm allocation.json

#associate and store association between elastic IP and instance
ASSOCIATION=$(/usr/bin/aws ec2 associate-address --instance-id $INSTANCE --allocation-id $ALLOCATION)
LOCALIP=$(curl http://169.254.169.254/latest/meta-data/local-ipv4)

#assign tags
/usr/bin/aws ec2 create-tags --resources $INSTANCE --tags "Key=Name,Value=cluster_primary"

#run primary, args are 1:ip 2:sampletableloc 3:spinuptableloc 4:procs 5:mem 6:s3 folder to store output
python 'aether/primary/main.py' $IP $1 $2 $3 $4 $5 $ALLOCATION $INSTANCE $LOCALIP $6 $7 $8 $9 2> primary.log

#the executation chain from primary.py will eventually end up self terminating this instance

