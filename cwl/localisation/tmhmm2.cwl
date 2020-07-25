#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [tmhmm]
hints:
  DockerRequirement:
    dockerImageId: tmhmm2

requirements:
  InlineJavascriptRequirement: {}


inputs:
  fastaFile:
    type: File
    label: Single protein FASTA file
    inputBinding:
      position: 1
    #format: edam:format_1929

  outputFilename:
    type: string?

outputs:
  outputSummary:
    type: stdout

  output:
    type: Directory
    outputBinding:
      glob: 'TMHMM*'

stdout: |
  ${
     if ( inputs.outputFilename != null){
     	return inputs.outputFilename;
     }
     else {
        return inputs.fastaFile.nameroot + ".tmhmm2.out";
     }
   }



$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.22.owl



