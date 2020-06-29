
############################
# Prerequisites !!!!!!!!!!!!
############################

# Be sure you have set the ${CrossSpeciesWorkflow_HOME} variable.
# As this variable is often used, it can be added to bashrc profile.

export CSW_HOME=/path/to/CSW/home


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

cd ${CSW_HOME}/dockerfiles/structural/psipred_disopred
docker build -t psipred_disopred_cpu -f psipred_disopred_cpu.dockerfile .

cd ${CSW_HOME}/dockerfiles/structural/raptorx
docker build -t raptorx_property_cpu -f raptorx_property_cpu.dockerfile .

cd ${CSW_HOME}/dockerfiles/structural/scratch1d
docker build -t scratch1d_cpu -f scratch1d_cpu.dockerfile .

cd ${CSW_HOME}/dockerfiles/structural/spot1d
docker build -t spot1d_cpu -f spot1d_cpu.dockerfile .


###############################
# B. Phosphorylation predictors
###############################

cd ${CSW_HOME}/dockerfiles/phosphorylation/dtu_predictors

cp ${netphospan_SOURCE}/netphospan-1.0* ${CSW_HOME}/dockerfiles/phosphorylation/dtu_predictors/
cp ${netphospan_SOURCE}/netphospan-1.0* ${CSW_HOME}/dockerfiles/phosphorylation/dtu_predictors/

docker build -t dtu_phosphorylation_cpu -f dtu_phosphorylation_cpu.dockerfile .    


cd ${CSW_HOME}/dockerfiles/phosphorylation/musitedeep

docker build -t musitedeep_keras2_tensorflow_cpu -f musitedeep_keras2_tensorflow_cpu.dockerfile .
docker build -t musitedeep_keras1_theano_cpu -f musitedeep_keras1_theano_cpu.dockerfile .

