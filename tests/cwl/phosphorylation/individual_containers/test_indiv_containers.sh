#!/usr/bin/ bash

RUNNER=cwltool

ARGS="--no-match-user --no-read-only"

CWLSCRIPTS=${CWL_HOME}/cwl/phosphorylation/indiv_predictors/

TESTFOLDER=${CWL_HOME}/tests/cwl/modules/phosphorylation/individual_containers/



# For each predictor folder, expected prediction outputs are provided in epected_output folders.


#########################################################
# Test netphos-3.1

cd $TESTFOLDER/netphos/
$RUNNER $ARGS $CWLSCRIPTS/netphos.cwl 1pazA.netphos.yml


#########################################################
# Test netphospan

cd $TESTFOLDER/netphospan/

# single protein, generic and kinase specific prediction
$RUNNER $ARGS $CWLSCRIPTS/netphospan_docker.cwl 1pazA.generic.netphospan.yml
$RUNNER $ARGS $CWLSCRIPTS/netphospan_docker.cwl 1pazA.PKACA.netphospan.yml

# multiple proteins, generic and kinase specific prediction
$RUNNER $ARGS $CWLSCRIPTS/netphospan_docker.cwl twoprot.generic.netphospan.yml
$RUNNER $ARGS $CWLSCRIPTS/netphospan_docker.cwl twoprot.PKACA.netphospan.yml



#########################################################
# Test musitedeep_keras1_theano

cd $TESTFOLDER/musitedeep1/

# single protein, generic and kinase specific prediction
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras1_theano_docker.cwl 1pazA.generic.musitedeep1.yml
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras1_theano_docker.cwl 1pazA.PKA.musitedeep1.yml

# multiple proteins, generic and kinase specific prediction
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras1_theano_docker.cwl twoprot.generic.musitedeep1.yml
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras1_theano_docker.cwl twoprot.PKA.musitedeep1.yml




#########################################################
# Test musitedeep_keras2_tensorflow

cd $TESTFOLDER/musitedeep2/

# single protein, generic and kinase specific prediction
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras2_tensorflow_docker.cwl 1pazA.generic.musitedeep2.yml
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras2_tensorflow_docker.cwl 1pazA.PKA.musitedeep2.yml

# multiple proteins, generic and kinase specific prediction
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras2_tensorflow_docker.cwl twoprot.generic.musitedeep2.yml
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras2_tensorflow_docker.cwl twoprot.PKA.musitedeep2.yml





