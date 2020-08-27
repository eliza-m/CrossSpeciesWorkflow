#!/usr/bin/env bash

########################################
# Please set the following variables
########################################


# Be sure you have previously set the ${CSW_HOME} variable.

# input folder where FASTA file is located
export inputFolder=${CSW_HOME}/tests/bash/single_protein/input

# protein name root ( in our example the FASTA file is 1pazA.fasta )
export prot="1pazA"

# output folder
export outputFolder=${CSW_HOME}/tests/bash/single_protein/output


############################################################
# RUN MUSITEDEEP v1 version (keras1 & theano)
############################################################

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



############################################################
# RUN MUSITEDEEP v2 version (keras2 & tensorflow)
############################################################

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



########################
# RUN NETPHOSPAN 
########################

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


########################
# RUN NETPHOS 3.1 
########################

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/phosphorylation/netphos:/output \
-e prot \
-it netphos-3.1:latest \
bash -c '\
/home/netphos-3.1/ape-1.0/ape /input/${prot}.fasta > /output/${prot}.netphos.out; '


########################
# ORGASNISE RESULTS
########################

# cd ${CSW_HOME}


