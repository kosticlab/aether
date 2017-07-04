""" Code to network the replica node."""
from os.path import join
import os
import sys
from socket import *
import thread


def networking_function():
    """
    This is a stub for testing the unit testing layout.
    """
    return 1


def parse_data(data):
    """
    Parses some data from the primary node.
    :param data: Message from the primary node
    :return: A 3-tuple containing: 1) Command received. 2) The node IP. 3) Command arguments.
    """
    (command, nodeIP, arguments) = data.split('\t')
    #TODO: Determine behavior (e.g., failure) for bad data formats.
    return (command, nodeIP, arguments)


def network(host, tasks, procsPerTask, memFracPerTask, outputLoc, primaryIP, allocation,
            instance, localIP):
    """
    This is a function that handles the networking for the replica node.
    :param host:
    :param tasks:
    :param procsPerTask:
    :param memFracPerTask:
    :param outputLoc:
    :param primaryIP:
    :param allocation:
    :param instance:
    :param localIP:
    :return: None
    """

    # TODO: Use absolute path for this.
    programPath = './program.sh'
    #TODO: Determine logDir value.
    logDir = ''

    port = 13001
    buff = 1024
    os.system("echo "+localIP+" >> localIP")
    addr = (localIP, port)
    ssock = socket(AF_INET, SOCK_STREAM)
    ssock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    ssock.bind(addr)
    ssock.listen(300)

    #run networking logic

    def handler(clientSock, addr):
        """
        Handles requests for the replica node.
        :param clientSock:
        :param addr:
        :return: None
        """
        data = clientSock.recv(buff)
        if len(data) > 0:
            os.system("echo {0} >> {1}".format(data, join(logDir, "networking.log")))
            command, node_ip, arguments = parse_data(data)
            if command == "assemble":
                os.system("echo received >> {0}".format(join(logDir, "assemble.log")))
                os.system("{0} {1} {2} {3} {4} {5} {6} 2> {7}&".format(
                    programPath, arguments, procsPerTask, memFracPerTask, host,
                    outputLoc, node_ip, join(logDir, "assemble.log")))
            if command == "exit":
                os.system("echo received >> {0}".format(join(logDir, "exit.log")))
                os.system("tar -czvf {0}.tar.gz {1}".format(instance, join(logDir, "*.log")))
                os.system("/usr/bin/aws s3 cp " +
                          "{0}.tar.gz s3://{1}/logs/".format(instance,outputLoc))
                os.system("/usr/bin/aws ec2 release-address --allocation-id " +
                          allocation)
                os.system("/usr/bin/aws ec2 terminate-instances " +
                          "--instance-ids {0}".format(instance))

    while 1:
        clientSock, addr = ssock.accept()
        thread.start_new_thread(handler, (clientSock, addr))


if __name__ == "__main__":
    for elem in sys.argv:
        os.system("echo "+elem+" >> args")
    network(*sys.argv[1:10])
