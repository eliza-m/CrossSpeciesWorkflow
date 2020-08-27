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

  outputNameroot:
    type: string
    inputBinding:
      position: 2
      prefix: -output


# Musitedeep offers either a generic phosphorylation prediction, or kinase-specific
# Supported kinases parameters are 'CDK', 'PKA', 'CK2', 'MAPK' or 'PKC'

  exclusive_parameters:

    type:
      - type: record
        fields:
          generalMode:
            type: string  # general
            inputBinding:
              prefix: -predict-type
              position: 3
          residues:
            type: string
            inputBinding:
              prefix: -residue-types # mutiple options 'S,T,Y' or single 'S' combinations
              position: 4

      - type: record
        fields:
          kinaseMode:
            type: string
            inputBinding:
              prefix: -predict-type
              position: 3
          customKinase:
            type: string
            inputBinding:
              prefix: -kinase
              position: 4


outputs:
  output:
    type:
      type: array
      items: File
    outputBinding:
      glob: '*.txt'

stdout: $(inputs.outputNameroot).log

$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.18.owl



