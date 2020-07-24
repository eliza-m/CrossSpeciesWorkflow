#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [netNglyc]
hints:
  DockerRequirement:
    dockerImageId: netnglyc-1.0d

inputs:

  fastaFile:
    type: File
    label: Single protein FASTA file
    inputBinding:
      prefix:
    #format: edam:format_1929

  outputFilename:
    type: string?

outputs:
  output:
    type: stdout

stdout: $(inputs.outputFilename)


$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.22.owl



