# get_SingleGeneSeq
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Author: "Wang Yansu"
# @Contanct: "Wangys_c@hotmail.com"
# @Time: "2019-7-30"
# @Version = "Version 1.0"
# @Discripton: "This script was designed to easily construct the species tree based on the single-copy gene obtained from the OrthoFinder results."
# @Discripton: "This script was designed to easily construct the species tree based on the single-copy gene based on concatenation method"
# @The script  originator is "Wei Dong" ("1369852697@qq.com") ,  Wang Yansu" modified it

import os
from optparse import OptionParser
import datetime
import subprocess
import re

############### MODIFY THE FOLLWINGS PATHS FOR ALL DEPENDENT PROGRAMS ###############
MAFFT = '/usr/bin/mafft'
TRIMAL = '/home/pub/software/trimAl/source/trimal'
RAxML = '/home/pub/software/RAxML/standard-RAxML/raxmlHPC'
#####################################################################################
def MakeOption():
    # make option
    parser = OptionParser(usage="%prog [-h] [-v] -t[--thread=] -n[--nb=] -m[--model=]]",
                          version="%prog 1.2")
    parser.add_option("-t", "--thread", action="store", dest="thread",
                      help="thread",
                      default=False)
    parser.add_option("-n", "--bootstrap", action="store", dest="bootstrap",
                      help="bootstrap",
                      default=False)
    parser.add_option("-m", "--model", action="store", dest="model",
                      help="model",
                      default=False)
    (options, args) = parser.parse_args()

    # extract option from command line
    thread= options.thread
    nb = options.bootstrap
    model = options.model
    return (thread,nb,model)
def run_command(cmd):
    # print("INFO: Running command: {0}".format(cmd), flush=True)
    print(cmd)
    return_code = subprocess.call(cmd, shell=True)
    if return_code != 0:
        print("ERROR: [{2}] Return code {0} when running the following command: {1}".format(return_code, cmd, datetime.datetime.now()))

def merge_SingleCopyGene():
	'''
	Merge every aligned single-copy gene into one super-gene matirx
	'''			
	filepath = "./"
	pathDir = os.listdir(filepath)
	name = []
	mydict2 = {}
	seq_file = []
	for allDir in pathDir:
		name.append(allDir)
	for i in range(len(name)):
		items = name[i]
		if ".fasta" in str(items):
			seq_file.append(str(items))
	for j in range(len(seq_file)):
		with open(str(seq_file[j])) as fh:
			for line in fh:
				if line.startswith(">"):
					seqid = line.strip(">").split(" ")[0].strip()
					if seqid not in mydict2.keys():
						mydict2[seqid] = []
				else:
					mydict2[seqid].append(line.strip())
	with open("merged_allSingleGenes.fasta","w") as fh:
		for key,value in mydict2.items():
			fh.write(">" + key + "\n" + "".join(value) + "\n")

def MLtree_Concatenation(thread,nb,model):
	'''
	Construct the ML species tree with the concatenate methold
	'''
	cmd1 = MAFFT + " --auto " + ' ./' + "merged_allSingleGenes.fasta" + ' >' + " merged_allSingleGenes_mafft.fasta"
	run_command(cmd1)
	cmd2 = TRIMAL + ' -in ' + " merged_allSingleGenes_mafft.fasta" + ' -out ' + " merged_allSingleGenes_mafft_trimal.fasta" + ' -automated1'
	run_command(cmd2)
	cmd = RAxML + ' -T ' + thread + ' -f a -N ' + nb + ' -m ' + model + ' -x 123456 -p 123456 -s ./merged_allSingleGenes_mafft_trimal.fasta -n concatenation_out.nwk'
	run_command(cmd)

def main():
	thread = MakeOption()[0]
	nb = MakeOption()[1]
	model = MakeOption()[2]
	merge_SingleCopyGene()
	MLtree_Concatenation(thread,nb,model)
if __name__ == '__main__':
	main()


