#!/usr/bin/ bash

RUNNER=cwltool

ARGS="--no-match-user --no-read-only"

CWLSCRIPTS=${CSW_HOME}/cwl/localisation/indiv_predictors/

TESTFOLDER=${CSW_HOME}/tests/cwl/test_individual_containers/localisation/



# For each predictor folder, expected prediction outputs are provided in epected_output folders.


#########################################################
# Test tmp_ssurface

cd $TESTFOLDER/tmp_ssurface/
$RUNNER $ARGS $CWLSCRIPTS/tmp_ssurface_docker.cwl ex1.tmp_ssurface.yml


#########################################################
# Test tmhmm2

# !!!!!!! 
# for unclear reasons it needs sudo to copy an output Folder from cwl temp folder to final output folder:

cd $TESTFOLDER/tmhmm2/
sudo $RUNNER $ARGS $CWLSCRIPTS/tmhmm2_docker.cwl ex1.tmhmm2.yml



#########################################################
# Test memsatsvm

cd $TESTFOLDER/memsatsvm/
$RUNNER $ARGS $CWLSCRIPTS/memsatsvm_from_mtx_docker.cwl 1LDI_A.memsatsvm.yml
$RUNNER $ARGS $CWLSCRIPTS/memsatsvm_from_mtx_docker.cwl 1M57_H.memsatsvm.yml



