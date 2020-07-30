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
export inputFolder=${CSW_HOME}/test/bash/single_protein/input

# protein name root ( in our example the FASTA file is 1pazA.fasta )
export prot="1pazA"

# output folder
export outputFolder=${CSW_HOME}/test/bash/single_protein/output

# CPU threads and maximum RAM (GB) to be used
export CPUnum=10
export maxRAM=16


####################
# RUN RAPTORX
####################

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


####################
# RUN SCRATCH1D
####################

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/structural/scratch1d:/output \
-e prot \
-e CPUnum \
-it scratch1d:latest bash -c '\
SCRATCH-1D_1.2/bin/run_SCRATCH-1D_predictors.sh /input/${prot}.fasta /output/${prot} ${CPUnum} ;' 


########################
# RUN PSIPRED 
########################

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


########################
# RUN DISOPRED 
########################

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



########################
# ORGASNISE RESULTS
########################

# cd ${CSW_HOME}

# needs refactoring !!!!!!!!!!!!!!
# python3 python/structural/SingleProtVerticalLayout.py 1pazA test/output/1pazA/ > test/output/StructuralPredVerticalLayout.txt


