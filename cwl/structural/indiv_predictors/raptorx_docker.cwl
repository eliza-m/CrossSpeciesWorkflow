#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [bash, /home/raptorx_cwl.sh]
hints:
  DockerRequirement:
    dockerPull: quay.io/dbsb-ibar/raptorx:latest

requirements:
  EnvVarRequirement:
    envDef:
      DBname: $(inputs.DBname)
      DBfolder: $(inputs.DBfolder.path)

# Mandatory arguments

inputs:
  fastaFile:
    type: File
    label: Single protein FASTA file
    #format: edam:format_1929
    inputBinding:
      position: 1

  DBname:
    type: string
    inputBinding:
      position: 2

  DBfolder:
    type: Directory


# Optional arguments

  SequenceProfileMethod:     # only the default hhblits3 was tested so far
    type: string?
    inputBinding:
      position: 3
    default: "hhsuite3"

  CPUthreads:
    type: int?
    inputBinding:
      position: 4
    default: 4

  RAMmax:                    # in GB
    type: int?
    inputBinding:
      position: 5
    default: 16


outputs:
  output:
    type:
      type: array
      items: File
    outputBinding: {glob: "*"}


$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.18.owl



