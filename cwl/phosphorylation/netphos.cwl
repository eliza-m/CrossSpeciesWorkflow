#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [/home/netphos-3.1/ape-1.0/ape]
hints:
  DockerRequirement:
    dockerImageId: dtu_phosphorylation_cpu:latest
    dockerOutputDirectory: /storage1/eliza/git/CrossSpeciesWorkflow/test/test_cwl
#   dockerOutputDirectory: $(runtime.outdir)

arguments: [$(inputs.fastaFile.path)]

inputs:
  fastaFile:
    type: File
    label: Single protein FASTA file
    #format: edam:format_1929

outputs:
  example_out:
    type: stdout

stdout: $(inputs.fastaFile.name).netphos


$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.18.owl



