#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [tcsh, /home/psipred/BLAST+/runpsipredplus]
hints:
  DockerRequirement:
    dockerPull: quay.io/dbsb-ibar/psipred:latest


requirements:
  InlineJavascriptRequirement: {}
  EnvVarRequirement:
    envDef:
      DBname: $(inputs.DBname)
      DBfolder: $(inputs.DBfolder.path)
      CPUnum: $(inputs.CPUnum)

inputs:
  fastaFile:
    type: File
    label: Single protein FASTA file
    #format: edam:format_1929
    inputBinding:
      position: 1

  DBname:
    type: string

  DBfolder:
    type: Directory

  CPUnum:
    type: int?
    default: 4    # This arg of psipred does not seem to directly work ?! I will look into it    


outputs:
  output:
    type:
      type: array
      items: File
    outputBinding: {glob: $(inputs.fastaFile.nameroot)*}


$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.18.owl



