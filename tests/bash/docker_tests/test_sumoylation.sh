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
# RUN DEEPSUMO_YL
############################################################

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/sumoylation/deepsumo_yl:/output \
-e prot \
-it deepsumo_yl:latest \
bash -c '\
python3 /home/DeepSUMO/codes/predict.py -input /input/${prot}.fasta \
-threshold 0.5 -output /output/${prot}.deepsumo_yl.out;'


############################################################
# RUN DEEPSUMO_REN
############################################################

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


########################
# ORGASNISE RESULTS
########################

# cd ${CSW_HOME}


