

export u20=/home/storage/eliza/uniprot20_2016_02
export output=$(pwd)/output
export input=$(pwd)/input

export prot="1pazA"
export CPUnum=10
export maxRAM=4

####################
# RUN RAPTORX
####################

docker run \
-v ${u20}:/home/TGT_Package/databases/uniprot20_2016_02 \
-v ${output}:/home/output -v ${input}:/home/input \
-e prot \
-e CPUnum \
-e maxRAM \
-it raptorx-property:latest bash -c \
'TGT_Package/A3M_TGT_Gen.sh -i input/${prot}.fasta -h hhsuite3 -d uniprot20_2016_02 -c ${CPUnum} -m ${maxRAM}; \
Predict_Property/Predict_Property.sh -i ${prot}_A3MTGT/${prot}.tgt; \
mkdir -p output/${prot}; \
mkdir -p output/${prot}/RaptorX; \
cp -r ${prot}_A3MTGT output/${prot}/RaptorX/ && \
cp -r ${prot}_PROP output/${prot}/RaptorX; ' 


####################
# RUN SCRATCH1D
####################

docker run \
-v ${output}:/home/output -v ${input}:/home/input \
-e prot \
-e CPUnum \
-it scratch1d:latest bash -c \
'mkdir -p output/${prot}; \
mkdir -p output/${prot}/Scratch1D; \
SCRATCH-1D_1.2/bin/run_SCRATCH-1D_predictors.sh input/${prot}.fasta output/${prot}/Scratch1D/${prot} ${CPUnum} ; \' 

