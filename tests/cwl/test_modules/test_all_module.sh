#!/usr/bin/env bash

RUNNER=cwltool

# Optionally "--parallel" flag can be added (with cautious to the Structural predictors that use a lot of RAM)

# Check if symlinks in ${CSW_HOME}/databases are set to your local sequence databases !!!!!!!!


ARGS="--no-match-user --no-read-only"

CWLSCRIPTS=${CSW_HOME}/cwl/


#########################################################

cd ${CSW_HOME}/tests/cwl/test_modules/

# Test Acetylation Module

$RUNNER $ARGS --outdir acetylation/1prot_fasta $CWLSCRIPTS/acetylation/1prot_acet_only_fasta.cwl 1prot_fasta.yml
$RUNNER $ARGS --outdir acetylation/1prot_id $CWLSCRIPTS/acetylation/1prot_acet_only_id.cwl 1prot_id.yml
$RUNNER $ARGS --outdir acetylation/Nprot_id $CWLSCRIPTS/acetylation/Nprot_acet_only_id.cwl Nprot_id.yml

# Test Glycosylation Module

$RUNNER $ARGS --outdir glycosylation/1prot_fasta $CWLSCRIPTS/glycosylation/1prot_glyc_only_fasta.cwl 1prot_fasta.yml
$RUNNER $ARGS --outdir glycosylation/1prot_id $CWLSCRIPTS/glycosylation/1prot_glyc_only_id.cwl 1prot_id.yml
$RUNNER $ARGS --outdir glycosylation/Nprot_id $CWLSCRIPTS/glycosylation/Nprot_glyc_only_id.cwl Nprot_id.yml

# Test Phosphorylation Module

$RUNNER $ARGS --outdir phosphorylation/1prot_fasta $CWLSCRIPTS/phosphorylation/1prot_phos_only_fasta.cwl 1prot_fasta.yml
$RUNNER $ARGS --outdir phosphorylation/1prot_id $CWLSCRIPTS/phosphorylation/1prot_phos_only_id.cwl 1prot_id.yml
$RUNNER $ARGS --outdir phosphorylation/Nprot_id $CWLSCRIPTS/phosphorylation/Nprot_phos_only_id.cwl Nprot_id.yml

# Test Lipid Module

$RUNNER $ARGS --outdir lipid/1prot_fasta $CWLSCRIPTS/lipid/1prot_lipid_only_fasta.cwl 1prot_fasta_lipid.yml
$RUNNER $ARGS --outdir lipid/1prot_id $CWLSCRIPTS/lipid/1prot_lipid_only_id.cwl 1prot_id.yml
$RUNNER $ARGS --outdir lipid/Nprot_id $CWLSCRIPTS/lipid/Nprot_lipid_only_id.cwl Nprot_id_lipid.yml

# Test Sumo Module

$RUNNER $ARGS --outdir sumoylation/1prot_fasta $CWLSCRIPTS/sumoylation/1prot_sumo_only_fasta.cwl 1prot_fasta.yml
$RUNNER $ARGS --outdir sumoylation/1prot_id $CWLSCRIPTS/sumoylation/1prot_sumo_only_id.cwl 1prot_id.yml
$RUNNER $ARGS --outdir sumoylation/Nprot_id $CWLSCRIPTS/sumoylation/Nprot_sumo_only_id.cwl Nprot_id.yml

# Test Localisation Module

$RUNNER $ARGS --outdir localisation/1prot_fasta $CWLSCRIPTS/localisation/1prot_loc_only_fasta.cwl 1prot_fasta.yml
$RUNNER $ARGS --outdir localisation/1prot_id $CWLSCRIPTS/localisation/1prot_loc_only_id.cwl 1prot_id.yml
$RUNNER $ARGS --outdir localisation/Nprot_id $CWLSCRIPTS/localisation/Nprot_loc_only_id.cwl Nprot_id.yml

# Test Structural Module

$RUNNER $ARGS --parallel --outdir structural/1prot_fasta $CWLSCRIPTS/structural/1prot_struct_only_fasta.cwl 1prot_fasta.yml
$RUNNER $ARGS --parallel --outdir structural/1prot_id $CWLSCRIPTS/structural/1prot_struct_only_id.cwl 1prot_id.yml
$RUNNER $ARGS --parallel --outdir structural/Nprot_id $CWLSCRIPTS/structural/Nprot_struct_only_id.cwl Nprot_id.yml


# Test PTM Module

$RUNNER $ARGS --outdir ptm/1prot_fasta $CWLSCRIPTS/1prot_ptm_fasta.cwl 1prot_fasta.yml
$RUNNER $ARGS --outdir ptm/1prot_id $CWLSCRIPTS/1prot_ptm_id.cwl 1prot_id.yml
$RUNNER $ARGS --outdir ptm/Nprot_id $CWLSCRIPTS/Nprot_ptm_id.cwl Nprot_id.yml

# Test All Module

$RUNNER $ARGS --outdir all/1prot_fasta $CWLSCRIPTS/1prot_all_fasta.cwl 1prot_fasta.yml
$RUNNER $ARGS --outdir all/1prot_id $CWLSCRIPTS/1prot_all_id.cwl 1prot_id.yml
$RUNNER $ARGS --outdir all/Nprot_id $CWLSCRIPTS/Nprot_all_id.cwl Nprot_id.yml




