#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [/home/netphos-3.1/ape-1.0/ape]
hints:
  DockerRequirement:
    dockerImageId: netphos-3.1:latest


inputs:
  fastaFile:
    type: File
    label: Single protein FASTA file
    inputBinding:
      position: 1
    #format: edam:format_1929

outputs:
  output:
    type: stdout
stdout: $(inputs.fastaFile.nameroot).netphos.out


$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.18.owl



