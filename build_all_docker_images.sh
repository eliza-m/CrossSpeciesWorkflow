
############################
# Prerequisites !!!!!!!!!!!!
############################

# Be sure you have set the ${CrossSpeciesWorkflow_HOME} variable.
# As this variable is often used, it can be added to bashrc profile.

export CrossSpeciesWorkflow_HOME=/path/to/CrossSpeciesWorkflow/home


# DTU predictors need registering before downloading the software !!!
# Please provide the path to the folder where DTU predictors source packages are being stored.

export netphospan_SOURCE=/path/to/netphospan/source
export netphos_SOURCE=/path/to/netphos/source


############################################
Build All docker images
############################################

############################
# A. Structural predictors
############################

cd ${CrossSpeciesWorkflow_HOME}/Dockerfiles/Structural

docker build -t psipred_cpu -f Psipred_CPU.Dockerfile .
docker build -t raptorx-property_cpu -f RaptorX-Property_CPU.Dockerfile .
docker build -t scratch1d_cpu -f Scratch1D_CPU.Dockerfile .
docker build -t spot1d_cpu -f Spot1D_CPU.Dockerfile .


###############################
# B. Phosphorylation predictors
###############################

cd ${CrossSpeciesWorkflow_HOME}/Dockerfiles/Phosphorylation/

docker build -t musitedeep_keras2_tensorflow_cpu -f MusiteDeep_keras2_tensorflow_CPU.Dockerfile .
docker build -t musitedeep_keras1_theano_cpu -f MusiteDeep_keras1_theano_CPU.Dockerfile .

cp ${netphospan_SOURCE}/netphospan-1.0* ${CrossSpeciesWorkflow_HOME}/Dockerfiles/Phosphorylation/
cp ${netphospan_SOURCE}/netphospan-1.0* ${CrossSpeciesWorkflow_HOME}/Dockerfiles/Phosphorylation/

docker build -t dtuhealthtech_phosphorylation_cpu -f DTUHealthTech_Phosphorylation_CPU.Dockerfile .    


