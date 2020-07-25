#!/usr/bin/ bash

RUNNER=cwltool

ARGS="--no-match-user --no-read-only"

CWLSCRIPTS=${CWL_HOME}/cwl/sumoylation/

TESTFOLDER=${CWL_HOME}/test/cwl/modules/sumoylation/



# For each predictor folder, expected prediction outputs are provided in epected_output folders.

#########################################################
# Test deepsumo_yl

cd $TESTFOLDER/deepsumo_yl/

# argument output name, multiple protein fasta file
$RUNNER $ARGS $CWLSCRIPTS/deepsumo_yl.cwl ex1.deepsumo_yl.yml

# generated output name, multiple protein fasta file
$RUNNER $ARGS $CWLSCRIPTS/deepsumo_yl.cwl ex2.deepsumo_yl.yml


#########################################################
# Test deepsumo_ren

cd $TESTFOLDER/deepsumo_ren/

# argument output name, multiple protein fasta file
$RUNNER $ARGS $CWLSCRIPTS/deepsumo_ren.cwl ex1.deepsumo_ren.yml

# generated output name, multiple protein fasta file
$RUNNER $ARGS $CWLSCRIPTS/deepsumo_ren.cwl ex2.deepsumo_ren.yml



