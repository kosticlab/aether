""" Code to network the primary node. """
from os.path import join, dirname
import os
import sys
import thread
from socket import *
import socket


def networking_function():
    """
    This is a stub for testing the unit testing layout.
    """
    return 1


def parse_data(data):
    """
    Parses some data from another node.
    :param data: Message from another node
    :return: A 3-tuple containing: 1) Command received. 2) The node IP. 3) Command arguments.
    """
    (command, nodeIP, arguments) = data.split('\t')
    #TODO: Determine behavior (e.g., failure) for bad data formats.
    return (command, nodeIP, arguments)



def network(host, sampleTableLoc, number, allocation, instance, localIP):
    """
    This is a function that handles networking on the primary node.
    :param host:
    :param sampleTableLoc:
    :param number:
    :param allocation:
    :param instance:
    :param localIP:
    :return: None.
    """
    port = 13001
    buff = 1024
    addr = (localIP, port)
    ssocket = socket.socket(AF_INET, SOCK_STREAM)
    ssocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    ssocket.bind(addr)
    ssocket.listen(2000)

    """ get lists of samples to process and info about what nodes to
        provision for processing job from s3 """
    os.system("/usr/bin/aws s3 cp {0} samples".format("s3://"+sampleTableLoc+"/arguments.dat"))
    samples = []

    """ make a list "samples" that contains arrays of length 2 corresponding to
        file locs for matched paired end reads """
    samples_file = open("samples", 'r')
    for line in samples_file:
        samples.append(line.rstrip())
    samples_file.close()

    global complete, jobs, number_replicas, replica_nodes


    """ run networking logic. note that the current iteration generates a logging file but does not
        automatically rerun potentially failed assemblies. need to test for packet loss also though
        this should not be an issue given that everything is in a datacenter """
    complete = 0
    jobs = len(samples)
    number_replicas = int(sys.argv[3])
    replica_nodes = set()


    def handler(clientsock, addr):
        global complete, jobs, number_replicas, replica_nodes
        #TODO: Determine logDir value.
        logDir = ""
        data = clientsock.recv(buff)
        if len(data) > 0:
            os.system("echo {0} >> {1}".format(data, join(logDir, "networking.log")))
            command, node_ip, arguments = parse_data(data)
            toaddr = (node_ip, 13001)
            if command == "complete":
                outgoing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                outgoing_socket.connect(toaddr)
                os.system("echo complete >> {0}".format(join(logDir, "complete.log")))
                complete += 1
                os.system("echo {0} {1} >> {2}".format(str(complete), arguments,
                                                       join(logDir, "completion.log")))
                if len(samples) > 0:
                    sample = samples.pop()
                    out = "assemble\t" + host + '\t' + sample
                    os.system("echo {0} >> {1}".format(out, join(logDir, "sent.log")))
                    outgoing_socket.send(out)
                outgoing_socket.close()
            if complete == jobs:
                for elem in replica_nodes:
                    outgoing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    outgoing_socket.connect(elem)
                    out = "exit\t" + host + "\texit"
                    os.system("echo {0} >> {1}".format(out, join(logDir, "sent.log")))
                    outgoing_socket.send(out)
                    outgoing_socket.close()
                os.system("tar -czvf primary{0}.tar.gz {1}".format(instance, join(logDir, "*.log")))
                os.system("/usr/bin/aws s3 cp " +
                          "{0}.tar.gz s3://{1}/logs/".format(instance,sampleTableLoc))
                os.system("/usr/bin/aws ec2 release-address --allocation-id " +
                          allocation)
                os.system("/usr/bin/aws ec2 terminate-instances " +
                          "--instance-ids {0}".format(instance))
            if command == "register":
                replica_nodes.add(toaddr)
                os.system("echo register >> {0}".format(join(logDir, "register.log")))
                for i in range(0, int(float(arguments))):
                    if len(samples) > 0:
                        outgoing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        outgoing_socket.connect(toaddr)
                        sample = samples.pop()
                        out = "assemble\t" + host + '\t' + sample
                        os.system("echo {0} >> {1}".format(out, join(logDir, "sent.log")))
                        outgoing_socket.send(out)
                    outgoing_socket.close()

    while 1:
        clientsock, addr = ssocket.accept()
        thread.start_new_thread(handler, (clientsock, addr))


if __name__ == "__main__":
    for elem in sys.argv:
        os.system("echo "+elem+" >> netargs")
    network(*sys.argv[1:7])
