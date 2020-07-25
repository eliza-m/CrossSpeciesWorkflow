#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [/home/netphospan-1.0.Linux/netphospan]
hints:
  DockerRequirement:
    dockerImageId: netphospan-1.0:latest

requirements:
  InlineJavascriptRequirement: {}


inputs:
  fastaFile:
    type: File
    label: Single/Multiple protein FASTA file
    #format: edam:format_1929
    inputBinding:
      position: 1
      prefix: -f

# Netphospan offers either a generic prediction, or kinase-specific
# A full list of supported kinases can be found : http://www.cbs.dtu.dk/services/NetPhospan/KIN_gene_names.txt

  exclusive_parameters:
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

  outputFilename:
    type: string?


outputs:
  output:
    type: stdout

stdout: |
  ${
     if ( inputs.outputFilename != ''){
     	return inputs.outputFilename;
     }
     else if ( inputs.exclusive_parameters.generic ) {
     	return inputs.fastaFile.nameroot + ".generic.netphospan.out";
     }
     else {
        return inputs.fastaFile.nameroot + "." + inputs.exclusive_parameters.kinase + ".netphospan.out";
     }
   }

$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.18.owl



