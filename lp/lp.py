import subprocess
import os
import json
from scipy.optimize import linprog
import sys
import pickle
import math
import numpy
from pandas import *

#this program will minimize cost per hour of distributed compute by utilizing Linear Programming to minimize cost/hour constrained by 1: minimum total cores desired at once, 2: minimum total RAM wanted at once, 3: minimum total free ephemeral storage desired, 4: AWS account limits, 5: variability in spot bidding price. Inherently, this considers both absolute cost of resources and risk of being outbid on the cheapest possible resources to optimize compute utilization.

class AWS_Instance:
    def __init__(self,procs,ram,eph,name,limit,running,running_spot,historical_max,current_spot,current_od):
        self.instance_type = name
        self.procs = procs
        self.ram = ram
        self.storage = eph
        self.limit = limit
        self.running = running
        self.running_spot = running_spot
        self.historical_max = historical_max
        self.current_od = current_od
        self.current_spot = current_spot

#params for constraints
def get_user_params():
    min_cores = int(raw_input("What is the minimum number of distributed cores required?"))
    min_ram = int(raw_input("What is the minimum amount in GB of distributed RAM required?"))
    min_free_storage = int(raw_input("What is the minimum amount in GB of free ephemeral storage required?"))
    max_cost_hour = float(raw_input("What is the max cost that you are willing to pay per hour for your virtual cluster?"))
    ram_per_job = int(raw_input("What amount of RAM is required per job?"))
    procs_per_job = int(raw_input("How many Processors are required per job?"))
    return min_cores,min_ram,min_free_storage,max_cost_hour,ram_per_job,procs_per_job

def handle_grep_non_zero_output(command):
    try:
        result = subprocess.check_output(command,shell=True)
        return result
    except subprocess.CalledProcessError as e:
        result = e.output
        return result

def define_A_matrix():
    current_time = int(subprocess.check_output("date +%s",shell=True))
    weeks_back = float(raw_input("How many weeks do you anticipate running your job for?"))
    start_time = int(current_time-(weeks_back*604800))
    eph = {}
    eph_file = open("resources/ephemeral_store_info.csv",'r')
    for line in eph_file:
        q = line.rstrip().split(',')
        eph_value = int(q[3])
        if eph_value > 0:
            eph[q[0]] = eph_value
    eph_file.close()
    retrievable_account_limits = set()
    gl_limits_file = open("resources/gamelift_instances.txt",'r')
    for line in gl_limits_file:
        retrievable_account_limits.add(line.rstrip())
    gl_limits_file.close()
    aws_instance_file = open("resources/instances.csv",'r')
    aws_instances = []
    os.system("aws ec2 describe-instances > ec2_instances.json")
    os.system("aws ec2 describe-spot-instance-requests > ec2_spot_instances.json")
    datacenters_fh = open("resources/datacenters.txt",'r')
    datacenters = []
    for lines in datacenters_fh:
        datacenters.append(lines.rstrip())
    for i in range(0,len(datacenters)):
        print(str(i+1)+" "+datacenters[i])
    datacenter_idx = int(raw_input("Please enter the integer corresponding to the amazon datacenter in which you are in:"))
    datacenter = datacenters[datacenter_idx-1]
    os.system("gunzip -c resources/odprices.gz > odprices")
    print("Please visit https://console.aws.amazon.com/ec2/v2/home?region=REGION#Limits: replacing REGION with the region in which you plan to run this scalable cluster in and provide the requested information that is not available in the API but critical for proper bidding when prompted.")
    idx = 0
    pickleq = raw_input("Would you like to use a pickle file?")
    if os.path.isfile(pickleq):
        aws_instances = pickle.load( open(pickleq,"rb"))
    else:
        for line in aws_instance_file:
            split_line = line.rstrip().split(',')
            instance_name = split_line[0]
            instance_ram_float = float(split_line[2])
            instance_procs_int = int(split_line[1])
            instance_eph_int = eph[instance_name] if eph.has_key(instance_name) else 0
            running_ec2 = int(subprocess.check_output("grep \""+instance_name+"\" ec2_instances.json | wc -l",shell=True))
            running_spot = int(subprocess.check_output("grep \""+instance_name+"\" ec2_spot_instances.json | wc -l",shell=True))
            if instance_name in retrievable_account_limits:
                os.system("aws gamelift describe-ec2-instance-limits --ec2-instance-type "+instance_name+" | jq -r '.EC2InstanceLimits[]' > i_temp.json")
                with open("i_temp.json",'r') as jsf:
                    gamelift_api_out = json.load(jsf)
                    instance_limit_pre = int(gamelift_api_out["InstanceLimit"])
                jsf.close()
            else:
                instance_limit_pre = int(raw_input("What is your account limit for "+instance_name+" in the current region being used?"))
            instance_limit = instance_limit_pre-running_spot
            historical_price_pre = handle_grep_non_zero_output("aws ec2 describe-spot-price-history --instance-types "+instance_name+" --end-time "+str(current_time)+" --start-time "+str(start_time)+" --product-descriptions='Linux/UNIX' --query 'SpotPriceHistory[*].{az:AvailabilityZone, price:SpotPrice}' | grep 'price' | sed 's/\"price\": \"//' | sed 's/^ *//' | sed 's/\",//' | uniq | sort | tail -1")
            historical_price = float(historical_price_pre)
            current_price_pre = float(handle_grep_non_zero_output("aws ec2 describe-spot-price-history --instance-types c4.large --start-time=$(date +%s) --product-descriptions=\"Linux/UNIX\" --query 'SpotPriceHistory[*].{az:AvailabilityZone, price:SpotPrice}' | grep 'price' | sed 's/\"price\": \"//' | sed 's/^ *//' | sed 's/\",//' | uniq | sort | tail -1"))
            current_price=float(current_price_pre)
            print("retrieved info for: "+instance_name)
            od_string = handle_grep_non_zero_output("cat odprices | grep '"+instance_name+"' | grep -v 'Reserved' | grep 'Shared' | grep -v 'SUSE' | grep -v 'Windows' | grep 'Linux' | grep '"+datacenter+"'")
            od_price = float(od_string.split(',')[9][1:-1])
            new_instance_type = AWS_Instance(instance_procs_int,instance_ram_float,instance_eph_int,instance_name,instance_limit,running_ec2,running_spot,historical_price,current_price,od_price)
            aws_instances.append(new_instance_type)
        pickle.dump( aws_instances, open("instances.p", "wb"))
        aws_instance_file.close()
    return aws_instances

#characteristics of compute nodes (A)
def formulate_problem(aws_instances):
    od_names = map(lambda name: name+".od",map(lambda instance_object: instance_object.instance_type, aws_instances))
    spot_names = map(lambda name: name+".spot",map(lambda instance_object: instance_object.instance_type, aws_instances))
    names = spot_names+od_names
    spot_prices = map(lambda instance_object: instance_object.current_spot, aws_instances)
    od_prices = map(lambda instance_object: instance_object.current_od, aws_instances)
    prices = spot_prices+od_prices
    procs_pre = map(lambda instance_object: instance_object.procs, aws_instances)
    procs = procs_pre+procs_pre
    gbRAM_pre = map(lambda instance_object: instance_object.ram, aws_instances)
    gbRAM = gbRAM_pre+gbRAM_pre
    freestorage_pre = map(lambda instance_object: instance_object.storage, aws_instances)
    #print freestorage_pre
    freestorage = freestorage_pre+freestorage_pre
    mc_pre = map(lambda instance_object: instance_object.historical_max, aws_instances)
    max_cost_in_previous_time_window = mc_pre+od_prices
    account_limits_pre = map(lambda instance_object: instance_object.limit, aws_instances)
    account_limits = account_limits_pre+account_limits_pre
    num_types = len(procs_pre)
    return num_types,names,prices,procs,gbRAM,freestorage,max_cost_in_previous_time_window,account_limits

#setting up LP problem formulation
def run_LP(num_types,names,prices,procs,gbRAM,freestorage,max_cost_in_previous_time_window,account_limits,min_cores,min_ram,min_free_storage,max_cost_hour,ram_per_job,procs_per_job,aws_instances):
    c = prices
    A_i = [procs,gbRAM,freestorage]
    b_i = [min_cores,min_ram,min_free_storage]
    A = map(lambda x: map(lambda y:y*-1,x),A_i)
    b = map(lambda z: z*-1,b_i)
    for i in range(0,num_types):
        append_a = [0] * num_types
        append_a[i] = 1
        add_a = append_a+append_a
        A.append(add_a)
        b.append(account_limits[i])
    A_limits = []
    b_limits = []
    for i in range(0,num_types):
        a_arr = [0]*num_types
        a_arr[i] = 1
        new_a = a_arr+a_arr
        A_limits.append(new_a)
        b_limits.append(account_limits[i])
    cost = 0
    status = 4
    while status != 0:
        A_t = A
        b_t = b
        if cost > max_cost_hour:
            break
        cost+=1
        A_t.append(max_cost_in_previous_time_window)
        b_t.append(cost)
        #print("solving:"+str(A_t)+"*x="+str(b_t))
        bounds_input = map(lambda x: (0,x),account_limits)
        lp_output = linprog(c,A_ub=A_t,b_ub=b_t,bounds=tuple(bounds_input))
        #print("x="+str(lp_output.x)+"\n\n")
        #lp_output = linprog(c,A_ub=A_t,b_ub=b_t,bounds=tuple(bounds_input),options={"bland": True})
	status=lp_output.status
        A_t.pop()
        b_t.pop()
        if status == 0:
            break
    lp_output_n = linprog(c,A_ub=A,b_ub=b,bounds=tuple(bounds_input),options={"bland": True})
    return lp_output,lp_output_n

def helper_recursive(input_item,names,instances):
    print input_item.x
    zipped_output = zip(names,input_item.x)
    filtered_output = filter(lambda x: x[1] != 0, zipped_output)
    remove_these_pre = map(lambda y: y[0], filter(lambda x: float(x[1]) < 1, filtered_output))
    remove_these = map(lambda x: '.'.join(x.split('.')[:2]), remove_these_pre)
    new_instances = filter(lambda x: x.instance_type not in remove_these,instances)
    return new_instances


def recursive_lp_n(lp_output,lp_output_n,min_cores,min_ram,min_free_storage,max_cost_hour,ram_per_job,procs_per_job,old_names,aws_instances):
    new_instances = helper_recursive(lp_output_n, old_names, aws_instances)
    num_types,names,prices,procs,gbRAM,freestorage,max_cost_in_previous_time_window,account_limits = formulate_problem(new_instances)
    new_lp_output, new_lp_output_n = run_LP(num_types,names,prices,procs,gbRAM,freestorage,max_cost_in_previous_time_window,account_limits,min_cores,min_ram,min_free_storage,max_cost_hour,ram_per_job,procs_per_job,new_instances)
    if type(new_lp_output_n.x)==float:
        return lp_output_n,old_names
    if len(new_lp_output_n.x) == 0:
        return lp_output_n,old_names
    if list(new_lp_output_n.x) == list(lp_output_n.x):
        return lp_output_n,old_names
    else:
        new_return = recursive_lp_n(new_lp_output,new_lp_output_n,min_cores,min_ram,min_free_storage,max_cost_hour,ram_per_job,procs_per_job,names,new_instances)
        return new_return

def recursive_lp(lp_output,lp_output_n,min_cores,min_ram,min_free_storage,max_cost_hour,ram_per_job,procs_per_job,old_names,aws_instances):
    new_instances = helper_recursive(lp_output, old_names, aws_instances)
    num_types,names,prices,procs,gbRAM,freestorage,max_cost_in_previous_time_window,account_limits = formulate_problem(new_instances)
    new_lp_output, new_lp_output_n = run_LP(num_types,names,prices,procs,gbRAM,freestorage,max_cost_in_previous_time_window,account_limits,min_cores,min_ram,min_free_storage,max_cost_hour,ram_per_job,procs_per_job,new_instances)
    if type(new_lp_output.x) == float:
        return lp_output,old_names
    elif len(new_lp_output.x) == 0:
        return lp_output,old_names
    elif list(new_lp_output.x) == list(lp_output.x):
        return lp_output,old_names
    else:
        new_return = recursive_lp(new_lp_output,new_lp_output_n,min_cores,min_ram,min_free_storage,max_cost_hour,ram_per_job,procs_per_job,names,new_instances)
        return new_return



#add filtering for running instances and job size
def start_bidding():
	min_cores,min_ram,min_free_storage,max_cost_hour,ram_per_job,procs_per_job = get_user_params()
	aws_instances = define_A_matrix()
        if min_free_storage > 0:
            aws_instances = filter(lambda x: x.storage > 0, aws_instances)
        aws_instances = filter(lambda x: x.procs > procs_per_job, aws_instances)
        aws_instances = filter(lambda x: x.ram > ram_per_job, aws_instances)
	num_types,old_names,prices,procs,gbRAM,freestorage,max_cost_in_previous_time_window,account_limits = formulate_problem(aws_instances)
	lp_output,lp_output_n = run_LP(num_types,old_names,prices,procs,gbRAM,freestorage,max_cost_in_previous_time_window,account_limits,min_cores,min_ram,min_free_storage,max_cost_hour,ram_per_job,procs_per_job,aws_instances)
	lp,names = recursive_lp(lp_output,lp_output_n,min_cores,min_ram,min_free_storage,max_cost_hour,ram_per_job,procs_per_job,old_names,aws_instances)
	lp_n,names_n = recursive_lp_n(lp_output,lp_output_n,min_cores,min_ram,min_free_storage,max_cost_hour,ram_per_job,procs_per_job,old_names,aws_instances)
	return lp,lp_n,names,names_n,aws_instances,min_cores,min_ram,min_free_storage,max_cost_hour,ram_per_job,procs_per_job

def find_provisioning_info(name,aws_instances):
    pre_desired_instance = filter(lambda x: x.instance_type == '.'.join(name.split('.')[:2]), aws_instances)
    assert(len(pre_desired_instance) == 1)
    desired_instance = pre_desired_instance[0]
    #print procs
    procs = str(desired_instance.procs)
    ram = str(int(desired_instance.ram))
    storage = desired_instance.storage
    name = '.'.join(name.split('.')[:2])
    return procs,ram,storage,name


def write_prov_file(lp_output,names,aws_instances):
    prov_file = open("prov.psv",'w')
    out_data = zip(names,lp_output.x)
    sum_deploy = 0
    for elem in out_data:
        pre_name = elem[0]
        procs,ram,storage,name = find_provisioning_info(pre_name,aws_instances)
        boolstr = "true" if storage > 0 else "false"
        number_to_deploy = int(round(float(elem[1])))
        sum_deploy += number_to_deploy
        for count in range(0,number_to_deploy):
            prov_file.write(name+'|'+procs+'|'+ram+'|'+boolstr+"|aws\n")
    prov_file.close()
    if sum_deploy == 0:
        sys.exit(1)
    return

def go():
    try:
        lp_output,lp_output_n,names,names_n,aws_instances,min_cores,min_ram,min_free_storage,max_cost_hour,ram_per_job,procs_per_job = start_bidding()
        write_prov_file(lp_output,names,aws_instances)
        return ram_per_job,procs_per_job
    except:
        print "No feasible solution found, try again with different parameters"

"""
if len(lp_output_n.x) > 0:
	naive_out = zip(names_n,lp_output_n.x)
	print "\n"
	print "Going by the seat of your pants and choosing the cheapest options that meet your criteria at the curren moment would result in this bid:"
	print filter(lambda x: x[1] != 0,naive_out)
else:
	print "There is no solution"
if len(lp_output) > 0:
	print "Taking in to account pricing variability, your ideal bid is:"
	cost_out = zip(names,lp_output.x)
	print filter(lambda x: x[1] != 0,cost_out)
"""
