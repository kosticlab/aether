#!/bin/bash
#script to add extra EBS storage---use as a template
#drive name must be xvd[b-z] or xvd[b-z][1-9]
instance=$(cat /var/lib/cloud/data/instance-id)
volume=$(aws ec2 create-volume --size $1 --availability-zone us-east-1d --volume-type gp2 | jq -r .VolumeId)
sleep 15
aws ec2 attach-volume --volume-id $volume --instance-id $instance --device $2
sleep 15
aws ec2 modify-instance-attribute --instance-id $instance --block-device-mappings "[{\"DeviceName\": \"$2\",\"Ebs\":{\"DeleteOnTermination\":true}}]"
sudo mkfs.ext4 /dev/$2
sudo mkdir /mnt/$2
sudo mount -t ext4 /dev/$2 /mnt/$2
sudo chown kosticlab /mnt/$2
