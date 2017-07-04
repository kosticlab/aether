from lp.lp import *
import os

ram_per_job,procs_per_job = go()
directory = raw_input("Please provide an absolute path to a file wherein each line " +
                     "corresponds" +
                     " to the directory of any data that the job script will need to access")
samples_file = raw_input("Please provide an absolute path to a file wherein each line " +
                     "corresponds" +
                     " to the argument for 1 job. Note that this line can be split with a" +
                     " delimiter in your job script if you need to pass multiple " +
                     "arguments, but avoid using spaces.")
project_name = raw_input("Please provide a name for the project. Note that this name should " +
                   "be unique" +
                   " because a corresponding S3 bucket will be created, and S3 buckets" +
                   " must be unique.")
aws_ID = raw_input("Please enter your AWS CLI Key ID.")
aws_key = raw_input("Please enter your AWS CLI Key.")
region = raw_input("Please provide your preferred region (e.g. us-east-1).")
script = raw_input("Please provide the script to be run on job inputs.")
os.system("./bin/initiate_compute.sh "+samples_file+" prov.psv "+procs_per_job+' '+ram_per_job+' '+project_name+' '+aws_ID+' '+aws_key+' '+region+' '+directory+' '+script)

