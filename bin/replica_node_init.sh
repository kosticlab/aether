#!/bin/bash

#simultaneous tasks, procs/task, mem frac/task, output loc, primaryIP, binary value for instance store

if [ "$6" == "true" ]
then
  sudo mkfs.ext4 /dev/xvdg
  sudo mkdir /mnt/hdrive
  sudo mount -t ext4 /dev/xvdg /mnt/hdrive
  sudo chown ubuntu /mnt/hdrive
fi

#get instance ID
INSTANCE=$(cat /var/lib/cloud/data/instance-id)

sleep 30
/usr/bin/aws s3 cp s3://$4/script/program.sh .
sudo chmod +x program.sh
/usr/bin/aws s3 cp s3://$4/bin/ bin --recursive
sudo chmod +x bin/*

#allocate elastic IP
/usr/bin/aws ec2 allocate-address --domain vpc > allocation.json

#get static IP and allocationID
IP=$(cat 'allocation.json' | jq -r .PublicIp)
ALLOCATION=$(cat 'allocation.json' | jq -r .AllocationId)

#associate and store association between elastic IP and instance
ASSOCIATION=$(/usr/bin/aws ec2 associate-address --instance-id $INSTANCE --allocation-id $ALLOCATION)
sleep 18
LOCALIP=$(curl http://169.254.169.254/latest/meta-data/local-ipv4)

#create tags
/usr/bin/aws ec2 create-tags --resources $INSTANCE --tags "Key=Name,Value=cluster_replica"

#run replica, args are 1:ownip, 2:tasks, 3:procs/task, 4:mem frac/task, 5:output loc, 6:primaryIP
python 'aether/replica/main.py' $IP $1 $2 $3 $4 $5 $ALLOCATION $INSTANCE $LOCALIP 2> replica.log



