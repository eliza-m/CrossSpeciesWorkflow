#!/usr/bin/env bash

########################################
# Please set the following variables
########################################

# Be sure you have previously set the ${CSW_HOME} variable.

# Location of the protein database to be use for generatig sequence profiles
# Please see the documentation provided in README.md file for each predictor

# for RaptorX the recommended db is uniprot20_2016_02 or uniclust30. For now, only the usage of uniprot20_2016_02 and hhsuite3 was tested.
export RaptorxDBfolder=/storage1/eliza/protDBs/uniprot20_2016_02

# for Psipred & DisoPred the recommended db is Uniref90 or Uniref50
export DBfolder=/storage1/eliza/protDBs/uniref50
export DBname=uniref50.fasta


# input folder where FASTA file is located
export inputFolder=${CSW_HOME}/tests/bash/single_protein/input

# protein name root ( in our example the FASTA file is 1pazA.fasta )
export prot="1pazA"

# output folder
export outputFolder=${CSW_HOME}/tests/bash/single_protein/output

# CPU threads and maximum RAM (GB) to be used
export CPUnum=10
export maxRAM=16


############################################################
# A. STRUCTURAL MODULE
############################################################

# RAPTORX

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/structural/raptorx:/output \
-v ${RaptorxDBfolder}:/home/TGT_Package/databases/uniprot20_2016_02 \
-e prot \
-e CPUnum \
-e maxRAM \
-it raptorx:latest bash -c '\
TGT_Package/A3M_TGT_Gen.sh -i /input/${prot}.fasta -h hhsuite3 -d uniprot20_2016_02 -c ${CPUnum} -m ${maxRAM} -o /output/; \
Predict_Property/Predict_Property.sh -i /output/${prot}.tgt -o /output/; '


# SCRATCH1D

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/structural/scratch1d:/output \
-e prot \
-e CPUnum \
-it scratch1d:latest bash -c '\
SCRATCH-1D_1.2/bin/run_SCRATCH-1D_predictors.sh /input/${prot}.fasta /output/${prot} ${CPUnum} ;' 


# PSIPRED 

docker run \
-v ${outputFolder}/structural/psipred:/output \
-v ${inputFolder}:/input \
-v ${DBfolder}:/home/database \
-e DBfolder=/home/database \
-e DBname \
-e prot \
-e CPUnum \
-it psipred:latest \
bash -c '\
cp /input/${prot}.fasta /output/ && cd /output/ ; \
$psipredplus /output/${prot}.fasta;'


# DISOPRED 

docker run \
-v ${outputFolder}/structural/disopred:/output \
-v ${inputFolder}:/input \
-v ${DBfolder}:/home/database \
-e DBfolder=/home/database \
-e DBname \
-e prot \
-e CPUnum \
-it disopred:latest \
bash -c '\
cp /input/${prot}.fasta /output/ && cd /output/ ; \
$disopredplus /output/${prot}.fasta;'




############################################################
# B. PHOSPHORYLATION MODULE
############################################################


# MUSITEDEEP v1 version (keras1 & theano)

# General predictor :

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/phosphorylation/musitedeep_keras1_theano:/output \
-e prot \
-it musitedeep_keras1_theano_cpu:latest \
bash -c '\
python predict.py -input /input/${prot}.fasta -output /output/ \
-predict-type general -residue-types S,T,Y ;'


# Kinase specific :

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/phosphorylation/musitedeep_keras1_theano:/output \
-e prot \
-it musitedeep_keras1_theano_cpu:latest \
bash -c '\
python predict.py -input /input/${prot}.fasta -output /output/ \
-predict-type kinase -kinase CDK ;'


# MUSITEDEEP v2 version (keras2 & tensorflow)

# General predictor :

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/phosphorylation/musitedeep_keras2_tensorflow:/output \
-e prot \
-it musitedeep_keras2_tensorflow_cpu:latest \
bash -c '\
python predict.py -input /input/${prot}.fasta -output /output/ \
-predict-type general -residue-types S,T,Y ;'


# Kinase specific :

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/phosphorylation/musitedeep_keras2_tensorflow:/output \
-e prot \
-it musitedeep_keras2_tensorflow_cpu:latest \
bash -c '\
python predict_batch.py -input /input/${prot}.fasta -output /output/ \
-predict-type kinase -kinase CDK ;'


# NETPHOSPAN 

# General predictor :

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/phosphorylation/netphospan:/output \
-e prot=$prot \
-it netphospan-1.0:latest \
bash -c '\
netphospan-1.0.Linux/netphospan -f /input/${prot}.fasta -generic > /output/${prot}.generic.netphospan.out;'

# Kinase specific :

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/phosphorylation/netphospan:/output \
-e prot=$prot \
-it netphospan-1.0:latest \
bash -c '\
netphospan-1.0.Linux/netphospan -f /input/${prot}.fasta -a PKACA > /output/${prot}.PKACA.netphospan.out;'


# NETPHOS 3.1 

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/phosphorylation/netphos:/output \
-e prot \
-it netphos-3.1:latest \
bash -c '\
/home/netphos-3.1/ape-1.0/ape /input/${prot}.fasta > /output/${prot}.netphos.out; '



############################################################
# C. GLYCOSYLATION MODULE
############################################################

# ISOGLYP

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/glycosylation/isoglyp:/output \
-e prot \
-it isoglyp \
bash -c '\
isoglypCL.py -p /home/ISOGlyP/isoPara.txt -f /input/${prot}.fasta ; \
mv isoglyp-predictions.csv /output/${prot}.isoglyp.out; '


# NETOGLYC

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/glycosylation/netoglyc:/output \
-e prot \
-it netoglyc-3.1:latest \
bash -c '\
netOglyc /input/${prot}.fasta > /output/${prot}.netoglyc.out; '


# NETNGLYC

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/glycosylation/netnglyc:/output \
-e prot \
-it netnglyc-1.0d:latest \
bash -c '\
netNglyc /input/${prot}.fasta > /output/${prot}.netnglyc.out; '


# NETCGLYC

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/glycosylation/netcglyc:/output \
-e prot \
-it netcglyc-1.0c:latest \
bash -c '\
netCglyc /input/${prot}.fasta > /output/${prot}.netcglyc.out; '


############################################################
# E. SUMOYLATION MODULE
############################################################

# DEEPSUMO_YL

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/sumoylation/deepsumo_yl:/output \
-e prot \
-it deepsumo_yl:latest \
bash -c '\
python3 /home/DeepSUMO/codes/predict.py -input /input/${prot}.fasta \
-threshold 0.5 -output /output/${prot}.deepsumo_yl.out;'


# DEEPSUMO_REN

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/sumoylation/deepsumo_ren:/output \
-e prot \
-e thresh_sumo="low" \
-e thresh_sim="low" \
-it deepsumo_ren:latest \
bash -c '\
python3 predict_main.py --t1 $thresh_sumo --t2 $thresh_sim \
-i /input/${prot}.fasta -o /output/ '




############################################################
# F. LOCALISATION MODULE
############################################################

# tmp_ssurface

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/localisation/tmp_ssurface:/output \
-e prot \
-it tmp_ssurface:latest \
bash -c '\
python3 run.py -f /input/${prot}.fasta -p /input/pssm/ -o /output/ ;'


# tmhmm2

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/localisation/tmhmm2:/output \
-e prot \
-it tmhmm2:latest \
bash -c '\
tmhmm /input/${prot}.fasta > /output/${prot}.tmhmm2.out; \
cp TMHMM_*/* /output/;'



# memsatsvm 

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/localisation/memsatsvm:/output \
-e prot \
-it memsatsvm:latest \
bash -c '\
./run_memsat-svm.pl -p 1 -g 0 -mtx 1 /input/pssm_mtx/${prot}.mtx -j /output/'


