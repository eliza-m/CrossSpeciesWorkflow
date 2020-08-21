#!/usr/bin/env bash

RUNNER=cwltool

ARGS="--no-match-user --no-read-only"

CWLSCRIPTS=${CSW_HOME}/cwl/

TESTFOLDER=${CSW_HOME}/tests/cwl/modules/glycosylation/

#########################################################
# Test 1prot workflow

cd $TESTFOLDER/output_1prot/

$RUNNER $ARGS $CWLSCRIPTS/1prot_glycopred.cwl 1prot.yml






