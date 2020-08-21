#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [isoglypCL.py, -p, /home/ISOGlyP/isoPara.txt]
hints:
  DockerRequirement:
    dockerPull: quay.io/dbsb-ibar/isoglyp

requirements:
  InlineJavascriptRequirement: {}

inputs:

  fastaFile:
    type: File
    label: Single/Multiple protein FASTA file
    inputBinding:
      prefix: -f
    #format: edam:format_1929

  outputFilename:
    type: string?


outputs:
  output:
    type: File
    outputBinding:
      glob: 'isoglyp-predictions.csv'
      outputEval: |
        ${
          if ( inputs.outputFilename != null){
             self[0].basename =  inputs.outputFilename;
          }
          else {
             self[0].basename =  inputs.fastaFile.nameroot + ".isoglyp.out";
          }
          return self[0]
        }

$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.22.owl



