#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [/home/SCRATCH-1D_1.2/bin/run_SCRATCH-1D_predictors.sh]
hints:
  DockerRequirement:
    dockerImageId: scratch1d:latest

requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
    listing:
      - entry: $(runtime.outdir)
        writable: true
      - entry: $(runtime.tmpdir)
        writable: true


inputs:
  fastaFile:
    type: File
    label: Single/Multiple protein FASTA file
    #format: edam:format_1929
    inputBinding:
      position: 1

  outputNameroot:
    type: string
    inputBinding:
      position: 2

  numthreads:
    type: int?
    inputBinding:
      position: 3
    

outputs:
  output:
    type:
      type: array
      items: File
    outputBinding:
      glob: '*.*'



$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.18.owl



