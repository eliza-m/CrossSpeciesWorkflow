#!/usr/bin/env cwl-runner

# Aligns protein FASTA sequences using clustalo
cwlVersion: v1.0
class: CommandLineTool
baseCommand: [clustalo]
hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/clustalo:1.2.4--he1b5a44_3

requirements:
  InlineJavascriptRequirement: {}

inputs:

  fastaFile:
  # Multi FASTA file
    type: File
    inputBinding:
      prefix: --in

  outputFilename:
    type: string?
    inputBinding:
      prefix: --out
    default: "prot.aln"


outputs:
  alnFile:
    type: File
    outputBinding:
      glob: '*.*'

$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.22.owl



