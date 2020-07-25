#!/usr/bin/ bash

RUNNER=cwltool

ARGS="--no-match-user --no-read-only"

CWLSCRIPTS=${CWL_HOME}/cwl/phosphorylation/

TESTFOLDER=${CWL_HOME}/test/cwl/modules/phosphorylation/



# For each predictor folder, expected prediction outputs are provided in epected_output folders.


#########################################################
# Test netphos-3.1

cd $TESTFOLDER/netphos/
$RUNNER $ARGS $CWLSCRIPTS/netphos.cwl 1pazA.netphos.yml


#########################################################
# Test netphospan

cd $TESTFOLDER/netphospan/

# single protein, generic and kinase specific prediction
$RUNNER $ARGS $CWLSCRIPTS/netphospan.cwl 1pazA.generic.netphospan.yml
$RUNNER $ARGS $CWLSCRIPTS/netphospan.cwl 1pazA.PKACA.netphospan.yml

# multiple proteins, generic and kinase specific prediction
$RUNNER $ARGS $CWLSCRIPTS/netphospan.cwl twoprot.generic.netphospan.yml
$RUNNER $ARGS $CWLSCRIPTS/netphospan.cwl twoprot.PKACA.netphospan.yml



#########################################################
# Test musitedeep_keras1_theano

cd $TESTFOLDER/musitedeep1/

# single protein, generic and kinase specific prediction
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras1_theano.cwl 1pazA.generic.musitedeep1.yml
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras1_theano.cwl 1pazA.PKA.musitedeep1.yml

# multiple proteins, generic and kinase specific prediction
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras1_theano.cwl twoprot.generic.musitedeep1.yml
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras1_theano.cwl twoprot.PKA.musitedeep1.yml




#########################################################
# Test musitedeep_keras2_tensorflow

cd $TESTFOLDER/musitedeep2/

# single protein, generic and kinase specific prediction
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras2_tensorflow.cwl 1pazA.generic.musitedeep2.yml
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras2_tensorflow.cwl 1pazA.PKA.musitedeep2.yml

# multiple proteins, generic and kinase specific prediction
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras2_tensorflow.cwl twoprot.generic.musitedeep2.yml
$RUNNER $ARGS $CWLSCRIPTS/musitedeep_keras2_tensorflow.cwl twoprot.PKA.musitedeep2.yml





