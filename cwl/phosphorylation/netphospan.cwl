#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [/home/netphospan-1.0.Linux/netphospan]
hints:
  DockerRequirement:
    dockerImageId: dtu_phosphorylation_cpu:latest
    dockerOutputDirectory: /storage1/eliza/git/CrossSpeciesWorkflow/test/test_cwl
#   dockerOutputDirectory: $(runtime.outdir)

inputs:
  fastaFile:
    type: File
    label: Single protein FASTA file
    #format: edam:format_1929
    inputBinding:
      position: 1
      prefix: -f

  exclusive_parameters:
    label: string
    type:
      - type: record
        name: generic
        fields:
          generic:
            type: boolean
            inputBinding:
              prefix: -generic
      - type: record
        name: kinase
        fields:
          kinase:
            type: string
            inputBinding:
              prefix: -a

outputs:
  example_out:
    type: stdout

stdout: $(inputs.fastaFile.name)_$(inputs.exclusive_parameters.label).netphospan


$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.18.owl



