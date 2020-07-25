#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [bash, /home/deepsumo.sh ]
hints:
  DockerRequirement:
    dockerImageId: deepsumo_ren

requirements:
  InlineJavascriptRequirement: {}

inputs:

  threshold_sumo:
    type: string # "low", "medium", "high", "all" or "none" 
    inputBinding:
     position: 1
    default: low

  threshold_sim:
    type: string # "low", "medium", "high", "all" or "none" 
    inputBinding:
      position: 2
    default: low

  fastaFile:
    type: File
    label: Single/Multiple protein FASTA file
    inputBinding:
      position: 3
    #format: edam:format_1929

  outputFilename:
    type: string?
    default: "temp.out"


outputs:
  output:
    type: File
    outputBinding:
      glob: 'output.txt'
      outputEval: |
        ${
          if ( inputs.outputFilename != "temp.out"){
             self[0].basename =  inputs.outputFilename;
          }
          else {
             self[0].basename =  inputs.fastaFile.nameroot + ".deepsumo_ren.out";
          }
          return self[0]
        }

$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.22.owl



