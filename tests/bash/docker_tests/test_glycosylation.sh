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
# RUN ISOGLYP
############################################################

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/glycosylation/isoglyp:/output \
-e prot \
-it isoglyp \
bash -c '\
isoglypCL.py -p /home/ISOGlyP/isoPara.txt -f /input/${prot}.fasta ; \
mv isoglyp-predictions.csv /output/${prot}.isoglyp.out; '



############################################################
# RUN NETOGLYC
############################################################

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/glycosylation/netoglyc:/output \
-e prot \
-it netoglyc-3.1:latest \
bash -c '\
netOglyc /input/${prot}.fasta > /output/${prot}.netoglyc.out; '


############################################################
# RUN NETNGLYC
############################################################

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/glycosylation/netnglyc:/output \
-e prot \
-it netnglyc-1.0d:latest \
bash -c '\
netNglyc /input/${prot}.fasta > /output/${prot}.netnglyc.out; '


############################################################
# RUN NETCGLYC
############################################################

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/glycosylation/netcglyc:/output \
-e prot \
-it netcglyc-1.0c:latest \
bash -c '\
netCglyc /input/${prot}.fasta > /output/${prot}.netcglyc.out; '



########################
# ORGASNISE RESULTS
########################

# cd ${CSW_HOME}


