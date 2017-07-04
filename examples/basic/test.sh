#!/bin/bash
echo $1 > file.$1.txt
sleep 30
/usr/bin/aws s3 cp file.$1.txt s3://$5/output/
./bin/terminate_job.sh $6 $1 $4
