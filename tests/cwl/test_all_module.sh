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







