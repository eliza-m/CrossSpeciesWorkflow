#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [bash, /home/scratch1d_cwl.sh]
hints:
  DockerRequirement:
    dockerPull: 193.231.158.8:5000/scratch1d:latest   # internal use
    # dockerImageId: scratch1d:latest                 # if built from Dockerfile

requirements:
  InlineJavascriptRequirement: {}


inputs:
  fastaFile:
    type: File
    label: Single/Multiple protein FASTA file
    #format: edam:format_1929
    inputBinding:
      position: 1

  outputNameroot:
    type: string
    inputBinding:
      position: 2

  numthreads:
    type: int?
    inputBinding:
      position: 3
    default: 4
    
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
  - http://edamontology.org/EDAM_1.18.owl



