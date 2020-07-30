
############################
# Prerequisites !!!!!!!!!!!!
############################

# Be sure you have set the CrossSpeciesWorkflow project home variable.
# As this variable is often used, it can be added to bashrc profile.

export CSW_HOME=/path/to/CSW/home


# DTU predictors need registering before downloading the software !!!
# Please provide the path to the folder where DTU predictors source packages are being stored.

# Phosphorylation module
export netphospan_SOURCE=/path/to/netphospan/source
export netphos_SOURCE=/path/to/netphos/source

# Glycosylation module
export netcglyc_SOURCE=/path/to/netcglyc/source
export netoglyc_SOURCE=/path/to/netoglyc/source
export netnglyc_SOURCE=/path/to/netnglyc/source
export sinalp_SOURCE=/path/to/sinalp/source

# Localisation module
export tmhmm_SOURCE=/path/to/tmhmm/source







############################################
Build All docker images
############################################

############################
# A. Structural predictors
############################

cd ${CSW_HOME}/dockerfiles/structural/psipred
docker build -t psipred -f psipred.dockerfile .

cd ${CSW_HOME}/dockerfiles/structural/disopred 
docker build -t disopred -f disopred .dockerfile .

cd ${CSW_HOME}/dockerfiles/structural/raptorx
docker build -t raptorx -f raptorx_property_cpu.dockerfile .

cd ${CSW_HOME}/dockerfiles/structural/scratch1d
docker build -t scratch1d -f scratch1d.dockerfile .

cd ${CSW_HOME}/dockerfiles/structural/spot1d
docker build -t spot1d -f spot1d_cpu.dockerfile .



###############################
# B. Phosphorylation predictors
###############################

cd ${CSW_HOME}/dockerfiles/phosphorylation/netphospan-1.0
cp ${netphospan_SOURCE}/netphospan-1.0* ${CSW_HOME}/dockerfiles/phosphorylation/netphospan-1.0/
docker build -t netphospan-1.0 -f netphospan-1.0.dockerfile .    

cd ${CSW_HOME}/dockerfiles/phosphorylation/netphos-3.1
cp ${netphos_SOURCE}/netphos-3.1* ${CSW_HOME}/dockerfiles/phosphorylation/netphos-3.1/
docker build -t netphos-3.1 -f netphos-3.1.dockerfile . 

cd ${CSW_HOME}/dockerfiles/phosphorylation/musitedeep
docker build -t musitedeep_keras2_tensorflow_cpu -f musitedeep_keras2_tensorflow_cpu.dockerfile .
docker build -t musitedeep_keras1_theano_cpu -f musitedeep_keras1_theano_cpu.dockerfile .



###############################
# C. Glycosylation predictors
###############################

cd ${CSW_HOME}/dockerfiles/phosphorylation/netcglyc-1.0c
cp ${netcglyc_SOURCE}/netcglyc-1* ${CSW_HOME}/dockerfiles/phosphorylation/netcglyc-1.0c/
docker build -t netcglyc-1.0c -f netcglyc-1.0c.dockerfile . 

cd ${CSW_HOME}/dockerfiles/phosphorylation/netoglyc-3.1
cp ${netoglyc_SOURCE}/netoglyc-3.1* ${CSW_HOME}/dockerfiles/phosphorylation/netoglyc-3.1/
cp ${signalp_SOURCE}/signalp* ${CSW_HOME}/dockerfiles/phosphorylation/netoglyc-3.1/
docker build -t netoglyc-3.1 -f netoglyc-3.1.dockerfile . 

cd ${CSW_HOME}/dockerfiles/phosphorylation/netnglyc-1.0d
cp ${netnglyc_SOURCE}/netnglyc-1* ${CSW_HOME}/dockerfiles/phosphorylation/netnglyc-1.0d/
cp ${signalp_SOURCE}/signalp* ${CSW_HOME}/dockerfiles/phosphorylation/netnglyc-1.0d/
docker build -t netnglyc-1.0d -f netnglyc-1.0d.dockerfile . 

cd ${CSW_HOME}/dockerfiles/phosphorylation/isoglyp
docker build -t isoglyp -f isoglyp.dockerfile . 


###############################
# D. Acetylation predictors
###############################

# On progress


###############################
# E. Cellular localisation predictors
###############################

cd ${CSW_HOME}/dockerfiles/localisation/tmp_ssurface
docker build -t tmp_ssurface -f tmp_ssurface.dockerfile . 

cd ${CSW_HOME}/dockerfiles/localisation/tmhmm2
cp ${tmhmm_SOURCE}/tmhmm-2.0c* ${CSW_HOME}/dockerfiles/localisation/tmhmm2/
docker build -t tmhmm2 -f tmhmm2.dockerfile . 

cd ${CSW_HOME}/dockerfiles/localisation/memsatsvm
docker build -t memsatsvm -f memsatsvm.dockerfile . 

# Phobius on progress....


###############################
# F. Sumoylation predictors
###############################

cd ${CSW_HOME}/dockerfiles/sumoylation/deepsumo_ren
docker build -t deepsumo_ren -f deepsumo_ren.dockerfile . 

cd ${CSW_HOME}/dockerfiles/sumoylation/deepsumo_yl
docker build -t deepsumo_yl -f deepsumo_yl.dockerfile . 


###############################
# G. Multiple PTS predictors
###############################

# On progress


