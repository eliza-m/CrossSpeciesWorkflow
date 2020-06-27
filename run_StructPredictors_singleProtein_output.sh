########################################
# Please set the following variables
########################################

# Be sure you have previously set the ${CrossSpeciesWorkflow_HOME} variable.

# Location of the protein database to be use for generatig sequence profiles
# Please see the documentation provided in README.md file for each predictor

# for RaptorX the recommended db is uniprot20_2016_02 or uniclust30. For now, only the usage of uniprot20_2016_02 and hhsuite3 was tested.
export RaptorxProtDB_PATH=/storage1/eliza/protDBs/uniprot20_2016_02
export RaptorxProtDB_NAME=uniprot20_2016_02

# for Psipred & DisoPred the recommended db is Uniref90 or Uniref50
export PsipredProtDB_PATH=/storage1/eliza/protDBs/uniref50
export PsipredProtDB_NAME=uniref50


# input folder where FASTA file is located
export inputFolder=${CrossSpeciesWorkflow_HOME}/input

# protein name root ( in our example the FASTA file is 1pazA.fasta )
export prot="1pazA"

# output folder
export outputFolder=${CrossSpeciesWorkflow_HOME}/output

# CPU threads and maximum RAM (GB) to be used
export CPUnum=10
export maxRAM=4


####################
# RUN RAPTORX
####################

docker run \
-v ${RaptorxProtDB_PATH}:/home/TGT_Package/databases/uniprot20_2016_02 \
-v ${outputFolder}:/output \
-v ${inputFolder}:/input \
-e prot \
-e CPUnum \
-e maxRAM \
-it raptorx-property_cpu:latest bash -c '\
mkdir -p /output/${prot}; \
mkdir -p /output/${prot}/RaptorX; \
TGT_Package/A3M_TGT_Gen.sh -i /input/${prot}.fasta -h hhsuite3 -d uniprot20_2016_02 -c ${CPUnum} -m ${maxRAM} -o /output/${prot}/RaptorX/${prot}_A3MTGT; \
Predict_Property/Predict_Property.sh -i /output/${prot}/RaptorX/${prot}_A3MTGT/${prot}.tgt -o /output/${prot}/RaptorX/${prot}_PROP; '\


####################
# RUN SCRATCH1D
####################

docker run \
-v ${outputFolder}:/output \
-v ${inputFolder}:/input \
-e prot \
-e CPUnum \
-it scratch1d_cpu:latest bash -c '\
mkdir -p output/${prot}; \
mkdir -p output/${prot}/Scratch1D; \
SCRATCH-1D_1.2/bin/run_SCRATCH-1D_predictors.sh /input/${prot}.fasta /output/${prot}/Scratch1D/${prot} ${CPUnum} ;' 


########################
# RUN PSIPRED 
########################

docker run \
-v ${PsipredProtDB_PATH}:/home/database/ \
-e ${PsipredProtDB_NAME}=${uniref_fastafile} \
-v ${outputFolder}:/output \
-v ${inputFolder}:/input \
-e prot=$prot \
-e RunNumOfThreads=$CPUnum \
-it psipred_cpu:latest \
bash -c '\
mkdir -p ${prot}; \
mkdir -p ${prot}/PsiPred; \
cp /input/${prot}.fasta /output/${prot}/PsiPred/ && cd ${prot}/PsiPred/ ;\
$psipredplus ${prot}.fasta;'


########################
# RUN DISOPRED 
########################

docker run \
-v ${PsipredProtDB_PATH}:/home/database/ \
-e ${PsipredProtDB_NAME}=${uniref_fastafile} \
-v ${outputFolder}:/output \
-v ${inputFolder}:/input \
-e prot=$prot \
-e RunNumOfThreads=$CPUnum \
-it psipred_cpu:latest \
bash -c '\
mkdir -p ${prot}; \
mkdir -p ${prot}/DisoPred; \
cp /input/${prot}.fasta /output/${prot}/DisoPred/ && cd ${prot}/DisoPred/ ;\
$disopredplus ${prot}.fasta;'


########################
# ORGASNISE RESULTS
########################

cd ${CrossSpeciesWorkflow_HOME}

python3 PythonAPI/Structural/SingleProtVerticalLayout.py 1pazA /output/1pazA/ > /output/1pazA/StructuralPredVerticalLayout.txt


