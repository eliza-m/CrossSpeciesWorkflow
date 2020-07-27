#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [bash, /home/tmp_ssurface_cwl.sh ]
hints:
  DockerRequirement:
    dockerImageId: tmp_ssurface

inputs:
  fastaFile:
    type: File
    label: Single protein FASTA file
    inputBinding:
      position: 1
    #format: edam:format_1929

  pssmFolder:
    type: Directory
    inputBinding:
      position: 2

  outputFolder:
    type: string
    inputBinding:
     position: 3


outputs:
  output:
    type:
      type: array
      items: File
    outputBinding:
      glob: "*.*"


$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.22.owl



