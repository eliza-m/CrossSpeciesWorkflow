#!/usr/bin/env cwl-runner

# Submits online jobs for any of the available predictors:
# Depending on the desired method define predictor variable as follows:
# (Glycosylation preds:) netcglyc, netnglyc, netoglyc, glycomine, nglyde
# (Phosphorylation pred:) netphos, ... 


cwlVersion: v1.0
class: CommandLineTool
baseCommand: [submit_online]
hints:
  DockerRequirement:
    dockerImageId: quay.io/dbsb-ibar/species_proteins:latest

requirements:
  InlineJavascriptRequirement: {}

inputs:

  predictor:
    type: string
    inputBinding:
      prefix: --predictor

  fastaFile:
    type: File
    label: Single protein FASTA file
    inputBinding:
      prefix: --input
    #format: edam:format_1929

  predtype:
    type: string?
    inputBinding:
      prefix: --type
    default: null

  outputFilename:
    type: string?
    inputBinding:
      prefix: --output
    default: "output.htm"


outputs:
  output:
    type: File
    outputBinding:
      glob: '*.*'
      outputEval: |
        ${
          if ( inputs.outputFilename != "output.htm"){
             self[0].basename =  inputs.outputFilename;
          }
          else if (inputs.predtype!=null) {
             self[0].basename =  inputs.fastaFile.nameroot + "." + inputs.predictor + inputs.predtype + ".htm";
          }
          else{
             self[0].basename =  inputs.fastaFile.nameroot + "." + inputs.predictor + ".htm";
          }
          return self[0]
        }

$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.22.owl



