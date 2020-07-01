#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [python, /home/MusiteDeep/MusiteDeep_Keras2.0/MusiteDeep/predict.py ]
hints:
  DockerRequirement:
    dockerImageId: musitedeep_keras2_tensorflow_cpu:latest
    dockerOutputDirectory: /storage1/eliza/git/CrossSpeciesWorkflow/test/test_cwl
#   dockerOutputDirectory: $(runtime.outdir)

inputs:
  fastaFile:
    type: File
    label: Single protein FASTA file
    #format: edam:format_1929
    inputBinding:
      position: 1
      prefix: -input

  outputFolder:
    type: string
    inputBinding:
      position: 2
      prefix: -output

  exclusive_parameters:
    label: string
    type:
      - type: record
        fields:
          generic:
            type: string
            inputBinding:
              prefix: -predict-type
          residues:
            type: string
            inputBinding:
              prefix: -residue-types

      - type: record
        fields:
          kinase:
            type: string
            inputBinding:
              prefix: -predict-type
          kinase:
            type: string
            inputBinding:
              prefix: -kinase

outputs:
  example_out:
    type: stdout

stdout: $(inputs.fastaFile.name)_$(inputs.exclusive_parameters.label).musite1


$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.18.owl



