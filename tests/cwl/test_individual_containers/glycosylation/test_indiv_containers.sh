#!/usr/bin/env bash

RUNNER=cwltool

ARGS="--no-match-user --no-read-only"

CWLSCRIPTS=${CSW_HOME}/cwl/glycosylation/indiv_predictors/

TESTFOLDER=${CSW_HOME}/tests/cwl/test_individual_containers/glycosylation/

# For each predictor folder, expected prediction outputs are provided in epected_output folders.

#########################################################
# Test netnglyc

cd $TESTFOLDER/netnglyc/

# given output name, single protein
$RUNNER $ARGS $CWLSCRIPTS/netnglyc_docker.cwl GLP.netnglyc.yml
$RUNNER $ARGS $CWLSCRIPTS/netnglyc_docker.cwl LEUK.netnglyc.yml

# generated output name, single protein
$RUNNER $ARGS $CWLSCRIPTS/netnglyc_docker.cwl CBG.netnglyc.yml

# generated output name, multiple proteins
$RUNNER $ARGS $CWLSCRIPTS/netnglyc_docker.cwl twoprot.netnglyc.yml


#########################################################
# Test isoglyp

cd $TESTFOLDER/isoglyp/

# generated output name, single protein
$RUNNER $ARGS $CWLSCRIPTS/isoglyp_docker.cwl CBG.isoglyp.yml

# given output name, single protein
$RUNNER $ARGS $CWLSCRIPTS/isoglyp_docker.cwl GLP.isoglyp.yml
$RUNNER $ARGS $CWLSCRIPTS/isoglyp_docker.cwl LEUK.isoglyp.yml

# generated output name, multiple proteins
$RUNNER $ARGS $CWLSCRIPTS/isoglyp_docker.cwl twoprot.isoglyp.yml


#########################################################
# Test netoglyc

cd $TESTFOLDER/netoglyc/

# generated output name, single protein
$RUNNER $ARGS $CWLSCRIPTS/netoglyc_docker.cwl CBG.netoglyc.yml

# given output name, single protein
$RUNNER $ARGS $CWLSCRIPTS/netoglyc_docker.cwl GLP.netoglyc.yml
$RUNNER $ARGS $CWLSCRIPTS/netoglyc_docker.cwl LEUK.netoglyc.yml

# generated output name, multiple proteins
$RUNNER $ARGS $CWLSCRIPTS/netoglyc_docker.cwl twoprot.netoglyc.yml


#########################################################
# Test netcglyc

cd $TESTFOLDER/netcglyc/

# generated output name, ONLY single protein fasta files are supported
$RUNNER $ARGS $CWLSCRIPTS/netcglyc_docker.cwl ATL5.netcglyc.yml



