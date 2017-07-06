#!/bin/bash
#Takes 10 args: 1:table with 1 argument per line corresponding to arguments for each run (s3 locs), 2:local table with 1 node spec per line, 3:procs to use for each assembly, 4:max memory that each assembly will use, 5:project name for s3 bucket, 6: aws access key ID, 7: aws secret access key, 8:desired AWS region, 9: file with binary locations, 10: execution script.  This will spin up a primary node, which will in turn spin up the provisioned fleet and communicate with the fleet over UDP to distribute the assemblies. Once this script is executed the distributed cluster is running. DO not submit multiple times without verifying failure on aws cloudwatch.


#configure CLI
printf "$6\n$7\n$8\n\n" | aws configure

#create s3 bucket for run
if [ $8 != "us-east-1" ]
then
  aws s3api create-bucket --bucket $5 --region $8 --create-bucket-configuration LocationConstraint=$8
else
  aws s3api create-bucket --bucket $5 --region $8
fi

BUCKET="s3://"$5

#upload binaries to s3.
#This is a tab delimited file with the first column being the folder and all subsequent columns being paths within that folder corresponding to binaries to be executed
aws s3 cp $9 $BUCKET/bin/ --recursive
aws s3 cp ${11} $BUCKET/data/ --recursive

echo $5 > name.txt
aws s3 cp name.txt $BUCKET/name/name.txt

aws s3 cp $1 $BUCKET/arguments.dat
aws s3 cp $2 $BUCKET/prov.psv

#upload script to s3.
aws s3 cp ${10} $BUCKET/script/program.sh

#create key pair
aws ec2 delete-key-pair --key-name $5
rm -rf "$5".pem
aws ec2 create-key-pair --key-name $5 | jq -r .KeyMaterial > "$5".pem
#sudo chmod 400 "$5".pem

#move key to s3
aws s3 cp "$5".pem $BUCKET/tempkey/

#find VPC
VPC=$(aws ec2 describe-vpcs | jq -r .Vpcs | jq '.[] | select(.IsDefault==true)' | jq -r .VpcId)

#create security group
aws ec2 delete-security-group --group-name $5 2> /dev/null
SECURITYGROUP=$(aws ec2 create-security-group --group-name $5 --description "security group" --vpc-id $VPC | jq -r .GroupId)


#modify security group rules
#allow ssh with temporary key to spin up nodes
aws ec2 authorize-security-group-ingress --group-id $SECURITYGROUP --protocol tcp --port 22 --cidr 0.0.0.0/0
#allow for the creation of TCP sockets between nodes
aws ec2 authorize-security-group-ingress --group-id $SECURITYGROUP --protocol tcp --port 13001 --cidr 0.0.0.0/0
echo $SECURITYGROUP > secgroup
aws s3 cp secgroup $BUCKET/security_group/
echo $8 > region
aws s3 cp region $BUCKET/region_info/

#create primary node instance configuration file
chmod +x bin/generate_instance_config.sh
bin/generate_instance_config.sh resources/template.json ami-80861296 $5 $SECURITYGROUP c4.large resources/primary.json

#Request a spot instance to serve as the primary node and parse the ID of the request, price granted will be market up to param
SPOTREQUEST=$(aws ec2 request-spot-instances --spot-price "5" --instance-count 1 --type "one-time" --launch-specification file://resources/primary.json | jq -r '.SpotInstanceRequests[]' | jq -r .SpotInstanceRequestId)

#Find the fulfilled ec2 instance associated with the previous spot request
while [ "$(aws ec2 describe-spot-instance-requests --spot-instance-request-ids $SPOTREQUEST | jq -r .SpotInstanceRequests[] | jq -r .InstanceId)" == "null" ];do sleep 1; done

#Find the instance ID
INSTANCEID=$(aws ec2 describe-spot-instance-requests --spot-instance-request-ids $SPOTREQUEST | jq -r .SpotInstanceRequests[] | jq -r .InstanceId)

#Find the IP address for this instance
IP=$(aws ec2 describe-instances --instance-ids $INSTANCEID | grep PublicDnsName | head -1 | awk -F ":" '{print $2}' | sed 's/[",]//g' | xargs)


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

#connect to the instance and execute pipeline, assuming that diabimmune repo is loaded in home dir of ami's utilized (does not need to current)
check_connection

chmod 400 "$5".pem
ssh -i "$5".pem -o StrictHostKeyChecking=no ubuntu@$IP 'sudo apt-get update; sudo apt-get install python awscli jq --assume-yes; printf "'${6}'\n'${7}'\n'${8}'\n\n" | /usr/bin/aws configure;/usr/bin/aws s3 cp s3://'$5'/tempkey/'$5'.pem .;sudo chmod 400 '$5'.pem; git clone git@github.com:kosticlab/aether.git;cd aether;cd bin;sudo chmod +x *.sh;cd ..;./bin/primary_node_init.sh '$1' '$2' '$3' '$4' '$5' '$6' '$7' '$9' '${10}' 2> error.log &'

