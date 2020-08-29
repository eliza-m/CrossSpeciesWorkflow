#!/usr/bin/env bash

RUNNER=cwltool

ARGS="--no-match-user --no-read-only"

CWLSCRIPTS=${CSW_HOME}/cwl/


#########################################################

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


# Test Structural Module

$RUNNER $ARGS --outdir structural/1prot_fasta $CWLSCRIPTS/structural/1prot_struct_only_fasta.cwl 1prot_fasta.yml
$RUNNER $ARGS --outdir structural/1prot_id $CWLSCRIPTS/structural/1prot_struct_only_id.cwl 1prot_id.yml


$RUNNER $ARGS --outdir structural/Nprot_id $CWLSCRIPTS/structural/Nprot_struct_only_id.cwl Nprot_id.yml







