""" Code to run the primary node. """
from __future__ import division
from os.path import join, dirname, abspath
import os
import sys
import math
from socket import *

def main_function():
    """
    This is a stub for testing the unit testing layout.
    """
    return 1


def run(host, sampleTableLoc, spinupTableLoc, procs, mem, outputDir, allocation, instance, localIP, awsLogin, awsPassword, azureLogin, azurePassword):
    """
    This is a function that runs the primary node.
    :param host:
    :param sampleTableLoc:
    :param spinupTableLoc:
    :param procs:
    :param mem:
    :param outputDir:
    :param allocation:
    :param instance:
    :param localIP:
    :param awsLogin
    :param awsPassword
    :param awsRegion
    :param azurePassword
    :return: None
    """
    #TODO: Determine logDir value.
    logDir = ""
    binPath = join(dirname(dirname(abspath(dirname(__file__)))), "bin")
    os.system("/usr/bin/aws s3 cp {0} provisioning".format("s3://"+outputDir+"/prov.psv"))
    provisioning = []
    with open("provisioning", 'r') as lineCount:
        for i, _ in enumerate(lineCount):
            pass
    # instantiate networking
    os.system("python {0} {1} {2} {3} {4} {5} {6} 2> {7} &".format(
        join(dirname(__file__), "networking.py"), host, outputDir, (i + 1), allocation,
        instance, localIP, join(logDir, "primary_networking.log")))
    os.system("sleep 30")


    def find_node_capability(node_procs, node_mem, task_procs, task_mem):
        """
        This is a function to find the optimal number of tasks that an arbitrary node is able
        to run concurrently and output number of tasks, node memory fraction, and number of
        threads to utilize per task.
        :param node_procs:
        :param node_mem:
        :param task_procs:
        :param task_mem:
        :return: A 3-tuple of 1) The number of tasks.
                              2) The node memory fraction.
                              3) The number of threads to utilize per task.
        """
        proc_tasks = math.floor(node_procs / task_procs)
        mem_tasks = math.floor(node_mem / task_mem)
        tasks = proc_tasks if proc_tasks < mem_tasks else mem_tasks
        mem_frac = ((node_mem / tasks) / (node_mem)) * 0.90
        threads = math.floor(node_procs / tasks)
        return str(int(float(tasks))), str(int(float(threads))), str(mem_frac)

    # parse and spin up fleet of replica nodes
    prov_file = open("provisioning", 'r')
    for line in prov_file:
        provisioning.append(line.rstrip().split('|'))
    prov_file.close()
    for elem in provisioning:
        instance_type = elem[0]
        cloud_provider = elem[4]
        tasks, threads, mem_frac = find_node_capability(float(elem[1]), float(elem[2]),
                                                        float(procs), float(mem))
        print(tasks, threads, mem_frac)
        if cloud_provider == "aws":
            os.system("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} &".format(
                join(binPath, "spinup_replica.sh"), instance_type, tasks, threads, mem_frac, outputDir,
                host, elem[3], awsLogin, awsPassword))
        if cloud_provider == "azure":
            id1=str(uuid.uuid4()).replace('-','')
            id2=str(uuid.uuid4()).replace('-','')
            id3=str(uuid.uuid4()).replace('-','')
            id4=str(uuid.uuid4()).replace('-','')
            id5=str(uuid.uuid4()).replace('-','')
            os.system("{0} {1}.json {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12}&".format(
                join(binPath, "spinup_replica_azure.sh"), elem[0], tasks, threads, mem_frac, outputDir,
                host, elem[3],id1,id2,id3,id4,id5,awsLogin,awsPassword,azureLogin,azurePassword))
if __name__ == "__main__":
    for elem in sys.argv:
        os.system("echo "+elem+" >> mainargs")
    run(*sys.argv[1:14])
