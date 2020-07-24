#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [python3, /home/DeepSUMO/codes/predict.py ]
hints:
  DockerRequirement:
    dockerImageId: deepsumo_yl

requirements:
  InlineJavascriptRequirement: {}

inputs:

  fastaFile:
    type: File
    label: Single protein FASTA file
    inputBinding:
      prefix: -input
    #format: edam:format_1929

  threshold:
    type: float
    inputBinding:
      prefix: -threshold
    default: 0.5

  outputFilename:
    type: string
    inputBinding:
      prefix: -output


outputs:
  output:
    type: File
    outputBinding:
      glob: '*.*'

$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.22.owl



