# Coalescence_Concatenation_tree
The originator of these scripts  is "Wei Dong" ("1369852697@qq.com") ,  Wang Yansu modified it.  This script was designed to easily construct the species tree based on the single-copy gene based on coalescence method and concatenation method

################

（1）不同物种相同基因为一个fasta,不同基因组成不同的fasta
 (2) 需要确保脚本和准备建树的fasta 文件在同一文件夹下，并保证文件夹下没有其他非建树所用的fasta文件
（3）需要修改脚本中所用到的软件路径

############### Coalescence.py #######################

python Coalescence.py -h 

such as : python Coalescence.py -t 10 -n 100 -m GTRGAMMA 

outputfile is Astral.coalescence_tree.nwk

########### Concatenation.py #########################

such as : python Concatenation.py -t 10 -n 100 -m GTRGAMMA

outputfile is concatenation_out.nwk
