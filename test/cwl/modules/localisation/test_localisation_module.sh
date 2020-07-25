#!/usr/bin/ bash

RUNNER=cwltool

ARGS="--no-match-user --no-read-only"

CWLSCRIPTS=${CWL_HOME}/cwl/localisation/

TESTFOLDER=${CWL_HOME}/test/cwl/modules/localisation/



# For each predictor folder, expected prediction outputs are provided in epected_output folders.

# Test tmp_ssurface

cd $TESTFOLDER/tmp_ssurface/
$RUNNER $ARGS $CWLSCRIPTS/tmp_ssurface.cwl ex1.tmp_ssurface.yml



# Test tmhmm2

# !!!!!!! 
# for unclear reasons it needs sudo to copy an output Folder from cwl temp folder to final output folder:


cd $TESTFOLDER/tmhmm2/
sudo $RUNNER $ARGS $CWLSCRIPTS/tmhmm2.cwl ex1.tmhmm2.yml



# Test memsatsvm

cd $TESTFOLDER/memsatsvm/
$RUNNER $ARGS $CWLSCRIPTS/memsatsvm_from_mtx.cwl 1LDI_A.memsatsvm.yml
$RUNNER $ARGS $CWLSCRIPTS/memsatsvm_from_mtx.cwl 1M57_H.memsatsvm.yml



