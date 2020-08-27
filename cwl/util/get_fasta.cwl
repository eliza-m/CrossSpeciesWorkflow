#!/usr/bin/env cwl-runner
 
cwlVersion: v1.0
class: CommandLineTool

baseCommand: [get-fasta]

hints:
  DockerRequirement:
    dockerPull: quay.io/dbsb-ibar/species_proteins:latest

inputs:

  uniprot:
    type: string
    inputBinding:
      prefix: --uniprot
    doc: |
      input Uniprot ID.

  trimheader:
    type: boolean
    inputBinding:
      prefix: --trimheader
    doc: |
      Trimm header ? True: use only ID as header; False: use original header. Default: False

  mode:
    type: string?
    inputBinding:
      prefix: --mode
    doc: |
      Saving mode: write (w) or append(a). Default 'w'

  outputfile:
    type: string?
    inputBinding:
      prefix: --output
    doc: |
      output filename. Default: '$uniprot.fasta' for 'w' mode and 'prot.fasta' for 'a' mode


outputs:
  fastaFile:
    type: File
    outputBinding:
      glob: '*.*'
    doc: |
      Output FASTA file


doc: |
  Tool runs species_proteins/run.py get-fasta to retrieve Fasta file from Uniprot ID
