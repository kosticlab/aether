import os
import sys
from socket import *
import socket

#ARGS 1:pe1loc,pe2loc 2:procs 3:mem frac 4:own ip 5:outputloc 6:primaryIP

#parse file names
paired_end_files = sys.argv[1]
pefs_arr = paired_end_files.split(',')
pe1 = pefs_arr[0]
pe2 = pefs_arr[1]
pe1_fname = pe1.split('/')[-1]
pe2_fname = pe2.split('/')[-1]
#added folder name
folder_name = pe2.split('/')[-2]


#download file names
if os.path.isdir("/mnt/hdrive"):
    os.chdir("/mnt/hdrive")

os.system("/usr/bin/aws s3 cp "+pe1+" ./"+pe1_fname)
os.system("/usr/bin/aws s3 cp "+pe2+" ./"+pe2_fname)
os.system("echo "+pe2_fname+" >> log")

#generate output folder names
#added folder name
#name = folder_name+pe1_fname.split('.')[0].split('_')[0]+'_'+pe1_fname.split('.')[0].split('_')[1]
name = folder_name+'_'+pe1_fname.split('.')[0].split('_')[0]
megahit_output= name+"_megahit"
prokka_output = name+"_prokka"

#run assembly and annotation
os.system("sudo bin/megahit/megahit -m "+sys.argv[3]+" --mem-flag 2 -t "+sys.argv[2]+" -1 "+pe1_fname+" -2 "+pe2_fname+" -o "+megahit_output+" 2> megahit.log")
os.system("sudo bin/prokka/bin/prokka --setupdb")
#mincontig len was 1000
os.system("sudo bin/prokka/bin/prokka --outdir "+prokka_output+" --prefix "+name+" --addgenes --metagenome --mincontiglen 1 --cpus "+sys.argv[2]+' '+megahit_output+"/final.contigs.fa"+" 2> prokka.log")

#copy results to s3 and cleanup
os.system("sudo mkdir "+name)
os.system("sudo mv "+megahit_output+' '+name)
os.system("sudo mv "+prokka_output+' '+name)
os.system("sudo /usr/bin/aws s3 cp "+name+"/ "+sys.argv[5]+name+"/ --recursive")
os.system("sudo rm -f "+pe1_fname)
os.system("sudo rm -f "+pe2_fname)
os.system("sudo rm -rf "+name)

#let primary node job is complete
host = sys.argv[6]
port = 13001
addr = (host, port)
tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsocket.connect(addr)
out = "complete\t"+sys.argv[4]+'\t'+name
os.system("echo "+out+" >> sent.log")
tcpsocket.send(out)
tcpsocket.close()

sys.exit(0)

