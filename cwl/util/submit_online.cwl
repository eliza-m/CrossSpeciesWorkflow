#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [submit-online]
hints:
  DockerRequirement:
    dockerPull: quay.io/dbsb-ibar/species_proteins:latest

requirements:
  InlineJavascriptRequirement: {}

inputs:

  predictor:
    type: string
    inputBinding:
      prefix: --predictor
    doc: |
      Depending on the selected method to use, define predictor variable as follows:
      (Glycosylation preds) netcglyc, netnglyc, netoglyc, glycomine, nglyde
      (Phosphorylation pred) netphos, netphospan
      (Acetylation pred) netacet, gpspail
      (Sumoylation pred) gpssumo, sumogo
      (Lipid pred) gpslipid
      (Localisation pred) tmhmm, tmpred

  fastaFile:
    type: File
    label: Single protein FASTA file
    inputBinding:
      prefix: --input
    #format: edam:format_1929
    doc: |
      Input FASTA file. It is advisable to trimm original headers as these are parsed differently between
      methods. Some predictors accept multi sequences FASTA files.

  predtype:
    type: string?
    inputBinding:
      prefix: --type
    default: null
    doc: |
      Some predictors require extra arguments.
      For the moment only glycomine requires this field: 'N', 'C' or 'O' depending on glycosylation type.

  outputFilename:
    type: string?
    inputBinding:
      prefix: --output
    default: "output.htm"
    doc: |
      Output filename.


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


doc: |
  Submits online jobs for any of the available predictors
  Depending on the desired method define predictor variable as follows:



