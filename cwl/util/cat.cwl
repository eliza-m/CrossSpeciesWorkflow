#!/usr/bin/env cwl-runner

cwlVersion: v1.0

class: CommandLineTool

baseCommand: cat

inputs:
  files:
    type: File[]
    inputBinding:
      position: 1

  outputname:
    type: string

outputs:
  output:
    type: stdout

stdout: $(inputs.outputname)