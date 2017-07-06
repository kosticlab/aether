#!/bin/bash

#ARGS: 1: json file for replica instance 2: number of "tasks" the node can handle simultaneously 3: procs/task 4:mem frac/task 5:output loc on s3 6: primaryIP 7:bool instance store


aws s3 cp s3://$5/name/name.txt .
aws s3 cp s3://$5/tempkey/$5.pem .
sudo chmod 400 $5.pem
aws s3 cp s3://$5/security_group/secgroup .
aws s3 cp s3://$5/region_info/region .
rm -rf resources/primary.json
bin/generate_instance_config.sh resources/template.json ami-80861296 $(cat name.txt) $(cat secgroup) $1 resources/primary.json
#Request a spot instance to serve as the primary node and parse the ID of the request
SPOTREQUEST=$(/usr/bin/aws ec2 request-spot-instances --spot-price "10" --instance-count 1 --type "one-time" --launch-specification file://resources/primary.json | jq -r .SpotInstanceRequests[] | jq -r .SpotInstanceRequestId)

#Find the fulfilled ec2 instance associated with the previous spot request
while [ "$(/usr/bin/aws ec2 describe-spot-instance-requests --spot-instance-request-ids $SPOTREQUEST | jq -r .SpotInstanceRequests[] | jq -r .InstanceId)" == "null" ];do sleep 1; done

#Find the instance ID
INSTANCEID=$(/usr/bin/aws ec2 describe-spot-instance-requests --spot-instance-request-ids $SPOTREQUEST | jq -r .SpotInstanceRequests[] | jq -r .InstanceId)

#Find the IP address for this instance
IP=$(/usr/bin/aws ec2 describe-instances --instance-ids $INSTANCEID | grep PublicDnsName | head -1 | awk -F ":" '{print $2}' | sed 's/[",]//g' | xargs)

#function to catch catch ssh connection refused errors if instance is still initializing. Note that this is some dirty code buy my hand was forced because amazon's instance status API is unreliable for the first 3 minutes after initialization
check_connection()
{
  (exec 3<>/dev/tcp/$IP/22) &>/dev/null
  if [ $? -ne 0 ]
  then
    sleep 30
    check_connection
  fi
}

#connect to the instance
check_connection
#simultaneous tasks, procs/task, mem frac/task, output loc, primaryIP
#sudo chmod 400 Kostic.pem
REG=$(cat region)
ssh -i "$5".pem -o StrictHostKeyChecking=no ubuntu@$IP 'sudo apt-get update; sudo apt-get install awscli jq python --assume-yes; printf "'${8}'\n'${9}'\n'$REG'\n\n" | /usr/bin/aws configure;/usr/bin/aws s3 cp s3://'$5'/tempkey/'$5'.pem .;sudo chmod 400 '$5'.pem; git clone git@github.com:kosticlab/diabimmune.git;cd diabimmune;git checkout jacob;cd bin;sudo chmod +x *.sh;cd ..;./bin/replica_node_init.sh '$2' '$3' '$4' '$5' '$6' '$7' 2> error.log &'


