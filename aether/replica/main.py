""" Code to run the replica node. """
from os.path import join, dirname
import os
import sys
from socket import *
import socket


def main_function():
    """
    This is a stub for testing the unit testing layout.
    """
    return 1


def run(host, tasks, procsPerTask, memFracPerTask, outputLoc, primaryIP, allocation,
        instance, localIP):
    """
    This is a function that runs the replica node.
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
    argStr = ' '.join(sys.argv[1:])
    #argStr = ' '.join([str(i) for i in locals().values()]) # do not move this line.
    #TODO: Determine logDir value.
    logDir = ""

    #os.system("sleep 15")
    os.system("python {0} {1} &".format(join(dirname(__file__), "networking.py"), argStr))
    os.system("sleep 20")
    port = 13001
    buf = 1024
    tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    m_addr = (primaryIP, port)
    tcpsocket.connect(m_addr)
    register_command = "register\t{0}\t{1}".format(host, tasks)
    os.system("echo {0} >> {1}".format(register_command, join(logDir, "sent.log")))
    tcpsocket.send(register_command)
    tcpsocket.close()

if __name__ == "__main__":
    for elem in sys.argv:
        os.system("echo "+elem+" >> mainarg")
    run(*sys.argv[1:10])
