########################################
# Please set the following variables
########################################

# Be sure you have previously set the ${CSW_HOME} variable.

# input folder where FASTA file is located
export inputFolder=${CSW_HOME}/test/input

# protein name root ( in our example the FASTA file is 1pazA.fasta )
export prot="1pazA"

# output folder
export outputFolder=${CSW_HOME}/test/output


############################################################
# RUN MUSITEDEEP v1 version (keras1 & theano)
############################################################

# General predictor :

docker run \
-v ${outputFolder}:/output \
-v ${inputFolder}:/input \
-e prot=$prot \
-it musitedeep_keras1_theano_cpu:latest \
bash -c '\
mkdir -p /output/${prot}/musitedeep_keras1_theano; \
python predict.py -input /input/${prot}.fasta \
-output /output/${prot}/musitedeep_keras1_theano/ \
-predict-type general -residue-types S,T,Y ;'


# Kinase specific :

docker run \
-v ${outputFolder}:/output \
-v ${inputFolder}:/input \
-e prot=$prot \
-it musitedeep_keras1_theano_cpu:latest \
bash -c '\
mkdir -p /output/${prot}/musitedeep_keras1_theano; \
python predict.py -input /input/${prot}.fasta \
-output /output/${prot}/musitedeep_keras1_theano/ \
-predict-type kinase -kinase CDK ;'



############################################################
# RUN MUSITEDEEP v2 version (keras2 & tensorflow)
############################################################

# General predictor :

docker run \
-v ${outputFolder}:/output \
-v ${inputFolder}:/input \
-e prot=$prot \
-it musitedeep_keras2_tensorflow_cpu:latest \
bash -c '\
mkdir -p /output/${prot}/musitedeep_keras2_tensorflow; \
python predict.py -input /input/${prot}.fasta \
-output /output/${prot}/musitedeep_keras2_tensorflow/ \
-predict-type general -residue-types S,T,Y ;'


# Kinase specific :

docker run \
-v ${outputFolder}:/output \
-v ${inputFolder}:/input \
-e prot=$prot \
-it musitedeep_keras2_tensorflow_cpu:latest \
bash -c '\
mkdir -p /output/${prot}/musitedeep_keras2_tensorflow; \
python predict.py -input /input/${prot}.fasta \
-output /output/${prot}/musitedeep_keras2_tensorflow/ \
-predict-type kinase -kinase CDK ;'



########################
# RUN NETPHOSPAN 
########################

# General predictor :

docker run \
-v ${outputFolder}:/output \
-v ${inputFolder}:/input \
-e prot=$prot \
-it dtu_phosphorylation_cpu:latest \
bash -c '\
mkdir -p /output/${prot}/netphospan; \
netphospan-1.0.Linux/netphospan -f /input/${prot}.fasta -generic > /output/${prot}/netphospan/generic.txt;'

# Kinase specific :

docker run \
-v ${outputFolder}:/output \
-v ${inputFolder}:/input \
-e prot=$prot \
-it dtu_phosphorylation_cpu:latest \
bash -c '\
mkdir -p /output/${prot}/netphospan; \
netphospan-1.0.Linux/netphospan -f /input/${prot}.fasta -a PKACA > /output/${prot}/netphospan/PKACA.txt;'


########################
# RUN NETPHOS 3.1 
########################

docker run \
-v ${outputFolder}:/output \
-v ${inputFolder}:/input \
-e prot=$prot \
-it dtu_phosphorylation_cpu:latest \
bash -c '\
mkdir -p /output/${prot}/netphos-3.1; \
/home/netphos-3.1/ape-1.0/ape /input/1pazA.fasta > /output/1pazA/netphos-3.1/netphos.txt ; '



########################
# ORGASNISE RESULTS
########################

cd ${CSW_HOME}


