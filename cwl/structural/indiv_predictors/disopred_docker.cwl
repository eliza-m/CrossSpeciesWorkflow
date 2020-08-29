#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [bash, /home/disopred/disopredplus_cwl.sh]
hints:
  DockerRequirement:
    dockerPull: quay.io/dbsb-ibar/disopred:latest

requirements:
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
    default: 4 # not sure if it works as expected
    

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



