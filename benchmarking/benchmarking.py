###benchmarking megahit
##20170516
#Tierney

###TODO:
#integrate with jacob's assembly measurement scripts
#maybe plot number of unaligned reads?
#determine which diabimmune data we should run through this


import sys
import subprocess
from ftplib import FTP
import numpy as np

#dependences: BLAT for pairwise alignment, ART_ILLUMINA for syn data generation, megahit, metaphlan2

###ARGUMENTS: paired end seq 1, paired end seq 2

#get data format and restructure arguments for metaphlan 
if sys.argv[1][-1:len(sys.argv[1])]=='a':
        ext='fasta'
else:
        ext='fastq'

if len(sys.argv)==3:
        args=','.join(sys.argv[1:3])

#run metaphlan on metagenome
subprocess.Popen('echo running metaphlan >> logfile.txt', shell=True,stdout=subprocess.PIPE).wait()
if ',' in args:
        process = subprocess.Popen('metaphlan2.py %s --bowtie2out %s_bowtie2out --input_type %s >> profiled_metagenome_%s.txt'%(args,args,ext,args),shell=True,stdout=subprocess.PIPE).wait()
else:
        process = subprocess.Popen('metaphlan2.py %s --input_type %s >> profiled_metagenome_%s.txt'%(args,ext,args),shell=True,stdout=subprocess.PIPE).wait()

subprocess.Popen('echo ...done >> logfile.txt', shell=True,stdout=subprocess.PIPE).wait()
#extract species names and percentages
subprocess.Popen('echo downloading reference genomes >> logfile.txt', shell=True,stdout=subprocess.PIPE).wait()
f=open('profiled_metagenome_%s.txt'%args,'rU')

species = []
for line in f:
        l=line.split('|')
        if len(l) == 7:
                print(l[6])
                name = l[-1].rstrip()
                species.append(name.split())

species=np.array(species)
#download reference genomes
genomes=[]
for i in range(0,len(species)):
        try:
                ftp = FTP('ftp.ncbi.nlm.nih.gov')
                ftp.login()
                ftp.cwd('/genomes/refseq/bacteria/%s/latest_assembly_versions/'%species[i,0][3:])
                file = ''.join(ftp.nlst()[0])
                ftp.cwd(file)
                filename = file + '_genomic.fna.gz'
                genomes.append(filename[:-3])
                ftp.retrbinary('RETR ' + filename, open(filename, 'wb').write)
                subprocess.Popen('gzip -d %s'%filename, shell=True,stdout=subprocess.PIPE).wait()
                ftp.close()

        except Exception as e:
                print(e)
                species = np.delete(species, (i), axis=0)
                continue

subprocess.Popen('echo ...done >> logfile.txt', shell=True,stdout=subprocess.PIPE).wait()


#find length of each genome to determine needed depth of sequencing
for j in range(0,len(genomes)):
        glengths=[]
        glengths.append(int(subprocess.Popen("awk 'NR>1' %s | wc -c"%genomes[j],shell=True,stdout=subprocess.PIPE).stdout.read()))

#calculate length percentages and relative coverage
total = sum(glengths)
maxSeqCov = 20
glengths = np.array([100*x/total for x in glengths])
depths = np.divide(glengths,species[:,1].astype(float))*maxSeqCov
print(depths)

#run art to generate synthetic metagenomes and concatenate 
subprocess.Popen('echo generating synthetic data >> logfile.txt', shell=True,stdout=subprocess.PIPE).wait()
subprocess.Popen('mkdir artout', shell=True,stdout=subprocess.PIPE).wait()
for h in range(0,len(genomes)):
        filename=genomes[h]
        subprocess.Popen('art_illumina -p -i %s -l 150 -f %i -m 1500 -s 10 -o artout/%s_'%(filename, depths[h],filename[:-4]),shell=True,stdout=subprocess.PIPE).wait()
        subprocess.Popen('cd artout && chmod +x * && cd ../',shell=True,stdout=subprocess.PIPE).wait()
        subprocess.Popen('paste artout/%s >> %s'%(filename[:-4]+'_1'+'.fq',sys.argv[1]+'_1.fq'),shell=True,stdout=subprocess.PIPE).wait()
        subprocess.Popen('paste artout/%s >> %s'%(filename[:-4]+'_2'+'.fq',sys.argv[2]+'_2.fq'),shell=True,stdout=subprocess.PIPE).wait()
subprocess.Popen('echo ...done >> logfile.txt', shell=True,stdout=subprocess.PIPE).wait()

#run megahit
subprocess.Popen('echo running megahit >> logfile.txt', shell=True,stdout=subprocess.PIPE).wait()
subprocess.Popen('megahit -1 %s -2 %s -o megahit_output >> logfile.txt'%(sys.argv[1]+'_1.fq',sys.argv[2]+'_2.fq'), shell=True,stdout=subprocess.PIPE).wait()
subprocess.Popen('echo ...done >> logfile.txt', shell=True,stdout=subprocess.PIPE).wait()

#create list of all contig labels
contigs = []
c = open('megahit_output/final.contigs.fa')
for line in c:
        if '>' in line:
                contigs.append(line[1:].split()[0])

contigs=set(contigs)

#concatenate all reference genomes for blat
for genome in genomes:
        subprocess.Popen('paste %s >> reference.fa'%genome,shell=True,stdout=subprocess.PIPE).wait()

subprocess.Popen('echo running blat >> logfile.txt', shell=True,stdout=subprocess.PIPE).wait()
#run blat to check contig alignment back to references
subprocess.Popen('blat reference.fa megahit_output/final.contigs.fa',shell=True,stdout=subprocess.PIPE).wait()
subprocess.Popen('pslReps output.psl bestAlign.psl out.psr',shell=True,stdout=subprocess.PIPE).wait()
subprocess.Popen('echo ...done >> logfile.txt', shell=True,stdout=subprocess.PIPE).wait()

psl=[]
sep=','

#parse blat output and find unaligned contigs
with open('bestAlign.psl','rU') as f:
        for i in range(0,5):
                next(f)
        for line in f:
                psl.append(line.split(sep,1)[0].split('\t'))
algn=pd.DataFrame(psl)

matched = set(algn.iloc[:,9])

unaligned = list(contigs-matched)

w=open('unalignedContigs.txt','w')
for line in unaligned:
        w.write('%s\n'%line)
subprocess.Popen('echo benchmarking completed >> logfile.txt', shell=True,stdout=subprocess.PIPE).wait()








