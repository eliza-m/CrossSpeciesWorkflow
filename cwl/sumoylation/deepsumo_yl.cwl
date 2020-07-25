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
    label: Single/Multiple protein FASTA file
    inputBinding:
      prefix: -input
    #format: edam:format_1929

  threshold:
    type: float
    inputBinding:
      prefix: -threshold
    default: 0.5

  outputFilename:
    type: string?
    inputBinding:
      prefix: -output
    default: "temp.out"


outputs:
  output:
    type: File
    outputBinding:
      glob: '*.*'
      outputEval: |
        ${
          if ( inputs.outputFilename != "temp.out"){
             self[0].basename =  inputs.outputFilename;
          }
          else {
             self[0].basename =  inputs.fastaFile.nameroot + ".deepsumo_yl.out";
          }
          return self[0]
        }


$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.22.owl



