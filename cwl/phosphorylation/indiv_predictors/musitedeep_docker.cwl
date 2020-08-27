#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [bash, /home/musitedeep2_cwl.sh ]
hints:
  DockerRequirement:
    dockerPull: quay.io/dbsb-ibar/musitedeep:keras2-tensorflow

requirements:
  InlineJavascriptRequirement: {}


inputs:
  fastaFile:
    type: File
    label: Single protein FASTA file
    #format: edam:format_1929
    inputBinding:
      position: 1
      prefix: -input
    doc: |
      input Uniprot ID.

  outputNameroot:
    type: string
    inputBinding:
      position: 2
      prefix: -output
    doc: |
      parsed data final output filename root. Suffixes will be added based on prediction type

  generalMode:
    type: string
    inputBinding:
      prefix: -predict-type
      position: 3
    default: general

  residues:
    type: string
    inputBinding:
      prefix: -residue-types # mutiple options 'S,T,Y' or single 'S' combinations
      position: 4

    doc: |
       Musitedeep offers either a generic phosphorylation prediction, or kinase-specific.
       Given the high number of kinases enzymes, for the main workflow
       we added only the "Generic" prediction mode. However, in indiv_containers folder:
       'musitedeep_keras1_theano_docker.cwl'
       and
       'musitedeep_keras2_tensorflow_docker.cwl'
       offer more usage freedom and can be used for kinase specific predictionds


outputs:
  output:
    type: File
    outputBinding:
      glob: '*.txt'
      outputEval: |
        ${
          if ( inputs.residues == "S,T"){
             var type = "ST";
          }
          else if ( inputs.residues == "Y") {
             var type = "Y";
          }
          else {
             var type = ""; 
          }
          self[0].basename =  inputs.outputNameroot + ".musitedeep" + type + ".txt";
          return self[0]
        }

    doc: |
      Predicted raw data


$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.18.owl



