#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [tmhmm]
hints:
  DockerRequirement:
    dockerImageId: tmhmm2

inputs:
  fastaFile:
    type: File
    label: Single protein FASTA file
    inputBinding:
      position: 1
    #format: edam:format_1929


outputs:
  outputSummary:
    type: stdout

  output:
    type: Directory
    outputBinding:
      glob: 'TMHMM*'

stdout: $(inputs.fastaFile.basename).out





$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.22.owl



