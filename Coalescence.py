# Coalescenece
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Modifier: "Wang Yansu"
# @Contanct: "Wangys_c@hotmail.com"
# @Time: "2019-8-1"
# @Version = "Version 1.0"
# @Discripton: "This script was designed to easily construct the species tree based on the single-copy gene based on coalescence method"
# @The script  originator is "Wei Dong" ("1369852697@qq.com") ,  Wang Yansu" modified it

from optparse import OptionParser
import subprocess
import datetime
import os

############### MODIFY THE FOLLWINGS PATHS FOR ALL DEPENDENT PROGRAMS ###############
MAFFT = '/usr/bin/mafft'
TRIMAL = '/home/pub/software/trimAl/source/trimal'
RAxML = '/home/pub/software/RAxML/standard-RAxML/raxmlHPC'
ASTRAL = '/home/pub/software/ASTRAL-master/Astral/astral.5.6.3.jar'
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

def MLtree_Coalescence(thread,nb,model):
    # Construct the ML species tree with the coalescent method
    #os.mkdir("Coalescence")
    # os.chdir("Coalescence")
    # 指定的目录
    path = "./"
    for item in os.listdir(path):
        if item.endswith(".fasta"):
            items = item.strip().split(".")
            seqfile = items[0] + ".fasta"
            seq_aln_file = items[0] + "_mafft.fasta"
            seq_aln_trimed_file = items[0] + "_mafft_trimed.fasta"
            cmd1 = MAFFT + " --auto " + ' ./' + seqfile + ' >' + seq_aln_file
            run_command(cmd1)
            cmd2 = TRIMAL + ' -in ' + seq_aln_file + ' -out ' + seq_aln_trimed_file + ' -automated1'
            run_command(cmd2)
            cmd3 = RAxML + ' -T ' + thread + ' -f a -N ' + nb + ' -m ' + model + ' -x 123456 -p 123456 -s ./' + seq_aln_trimed_file + ' -n ' + items[0]
            run_command(cmd3)
            cmd4 = 'cat RAxML_bipartitions.' + items[0] + ' >>allSingleGenes_tree.nwk'
            run_command(cmd4)
            cmd5 = 'echo ./RAxML_bootstrap.' + items[0] + ' >>allSingleGenes_bootstrap.txt'
            run_command(cmd5)

    cmd6 = 'java -jar ' + ASTRAL +' -i allSingleGenes_tree.nwk -b allSingleGenes_bootstrap.txt -r ' + nb + ' -o Astral.coalescent_out.result'
    run_command(cmd6)
    os.system('tail -n 1 Astral.coalescent_out.result >Astral.coalescence_tree.nwk')

def main():
    thread = MakeOption()[0]
    nb = MakeOption()[1]
    model = MakeOption()[2]
    MLtree_Coalescence(thread, nb, model)
if __name__ == "__main__":
   main()
