#!/usr/bin/ bash

RUNNER=cwltool

ARGS=--no-read-only

CWLSCRIPTS=${CWL_HOME}/cwl/glycosylation/

TESTFOLDER=${CWL_HOME}/test/cwl/modules/glycosylation/



# For each predictor folder, expected prediction outputs are provided in epected_output folders.

# Test netnglyc-1.0d

cd $TESTFOLDER/netnglyc/
$RUNNER $ARGS $CWLSCRIPTS/netnglyc.cwl CBG.netnglyc.yml
$RUNNER $ARGS $CWLSCRIPTS/netnglyc.cwl GLP.netnglyc.yml
$RUNNER $ARGS $CWLSCRIPTS/netnglyc.cwl LEUK.netnglyc.yml
$RUNNER $ARGS $CWLSCRIPTS/netnglyc.cwl twoprot.netnglyc.yml


# Test isoglyp

cd $TESTFOLDER/isoglyp/
$RUNNER $ARGS $CWLSCRIPTS/isoglyp.cwl CBG.isoglyp.yml
$RUNNER $ARGS $CWLSCRIPTS/isoglyp.cwl GLP.isoglyp.yml
$RUNNER $ARGS $CWLSCRIPTS/isoglyp.cwl LEUK.isoglyp.yml
$RUNNER $ARGS $CWLSCRIPTS/isoglyp.cwl twoprot.isoglyp.yml

# Test netoglyc-3.1

cd $TESTFOLDER/netoglyc/
$RUNNER $ARGS $CWLSCRIPTS/netoglyc.cwl CBG.netoglyc.yml
$RUNNER $ARGS $CWLSCRIPTS/netoglyc.cwl GLP.netoglyc.yml
$RUNNER $ARGS $CWLSCRIPTS/netoglyc.cwl LEUK.netoglyc.yml
$RUNNER $ARGS $CWLSCRIPTS/netoglyc.cwl twoprot.netoglyc.yml


# Test netcglyc-1.0c

cd $TESTFOLDER/netcglyc/
$RUNNER $ARGS $CWLSCRIPTS/netcglyc.cwl ATL5.netcglyc.yml



