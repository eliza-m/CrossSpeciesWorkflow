########################################
# Please set the following variables
########################################

# Be sure you have previously set the ${CSW_HOME} variable.

# input folder where FASTA file is located
export inputFolder=${CSW_HOME}/test/bash/single_protein/input

# protein name root ( in our example the FASTA file is 1pazA.fasta )
export prot="1pazA"

# output folder
export outputFolder=${CSW_HOME}/test/bash/single_protein/output


############################################################
# RUN tmp_ssurface
############################################################

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/localisation/tmp_ssurface:/output \
-e prot \
-it tmp_ssurface:latest \
bash -c '\
python3 run.py -f /input/${prot}.fasta -p /input/pssm/ -o /output/ ;'


############################################################
# RUN tmhmm2
############################################################

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/localisation/tmhmm2:/output \
-e prot \
-it tmhmm2:latest \
bash -c '\
tmhmm /input/${prot}.fasta > /output/${prot}.tmhmm2.out; \
cp TMHMM_*/* /output/;'



############################################################
# RUN memsatsvm
############################################################

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/localisation/memsatsvm:/output \
-e prot \
-it memsatsvm:latest \
bash -c '\
./run_memsat-svm.pl -p 1 -g 0 -mtx 1 /input/pssm_mtx/${prot}.mtx -j /output/'



########################
# ORGASNISE RESULTS
########################

# cd ${CSW_HOME}


