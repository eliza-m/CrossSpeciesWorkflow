#!/usr/bin/env bash


# !!!!!!!!!!!!!!!!!
# Before running this script please be sure that the symbolic links in the
# databases folder are set accordingly
# This is needed as an workaround for cwl-runner that redefines $HOME variable 
# according to the final output directory and cannot directly access other 
# paths from host. Please see bellow what databases require symbolic links.


RUNNER=cwltool

ARGS="--no-match-user --no-read-only"

CWLSCRIPTS=${CWL_HOME}/cwl/structural/

TESTFOLDER=${CWL_HOME}/tests/cwl/modules/structural/



# For each predictor folder, expected prediction outputs are provided in epected_output folders.


#########################################################
# Test scratch1d

cd $TESTFOLDER/scratch1d/

# test single protein fasta file
$RUNNER $ARGS $CWLSCRIPTS/scratch1d.cwl 1pazA.scratch1d.yml

# test multiple protein fasta file
$RUNNER $ARGS $CWLSCRIPTS/scratch1d.cwl twoprot.scratch1d.yml



#########################################################
# Test psipred

# !!!! Please make sure that the symbolic links from the databases folder are set accordingly

# ln -s /path/to/host/db/folder/uniref50 ${CWL_HOME}/test/cwl/modules/structural/databases/uniref50

cd $TESTFOLDER/psipred/

# Only single protein fasta file format is supported
$RUNNER $ARGS $CWLSCRIPTS/psipred.cwl 1pazA.psipred.yml


#########################################################
# Test disopred

# !!!! Please make sure that the symbolic links from the databases folder are set accordingly

# ln -s /path/to/host/db/folder/uniref50 ${CWL_HOME}/test/cwl/modules/structural/databases/uniref50

cd $TESTFOLDER/disopred/

# Only single protein fasta file format is supported
$RUNNER $ARGS $CWLSCRIPTS/disopred.cwl 1pazA.disopred.yml



#########################################################
# Test raptorx

# !!!! Please make sure that the symbolic links from the databases folder are set accordingly.
# These are required only for building the profile (raptorx_profile.cwl)

# ln -s /path/to/host/db/folder/uniprot20_2016_02 ${CWL_HOME}/test/cwl/modules/structural/databases/uniprot20_2016_02

cd $TESTFOLDER/raptorx/

# on progress....

