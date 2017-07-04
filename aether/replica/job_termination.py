import os
import sys
from socket import *
import socket

host = sys.argv[1]
os.system("echo "+host+" > host")
port = 13001
addr = (host, port)
tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsocket.connect(addr)
out = "complete\t"+sys.argv[3]+'\t'+sys.argv[2]
os.system("echo "+out+" >> sent.log")
tcpsocket.send(out)
tcpsocket.close()
sys.exit(0)
