#!/usr/bin/env cwl-runner


  # As Memsatsvm is compatible only with legacy blast we only considered the usage of
  # already precomputed mtx files with blast+ or other software such as hmmer or hhsuite
  # as these are already used by other predictors included in this repo and can be passed
  # directly to memsatsvm and save a lot of time.
  # Also, there are some unsolved errors when using the topology drawing and we disabled it.


cwlVersion: v1.0
class: CommandLineTool
baseCommand: [/home/MemSatSVM/run_memsat-svm.pl]
arguments: ["-w", "/home/MemSatSVM", "-mtx", "1", "-g", "0", "-j", $(runtime.outdir)]
hints:
  DockerRequirement:
    dockerImageId: memsatsvm


inputs:

  # Programs to run. memsat-svm predicts topology, globmem-svm
  #             discriminates between transmembrane and globular proteins. Default 0.
  #             0 = Run memsat-svm
  #             1 = Run memsat-svm and globmem-svm
  #             2 = Run globmem-svm
  predType:
    type: int
    inputBinding:
      prefix: -p      
      position: 1
    default: 1

  # -s <0|1>       Run memsat-svm with signal peptide function. Default: 1
  signalPeptide:
    type: int
    inputBinding:
      prefix: -s      
      position: 2
    default: 1

  #-3 <0|1|2>     Run memsat version 3. Default 0.
  #             0 = Run memsat-svm
  #             1 = Run memsat-svm and memsat3
  #             2 = Run memsat3
  version:
    type: int
    inputBinding:
      prefix: "-3"      
      position: 3
    default: 1

  # Output filename when running a single sequence. Default: <fasta file>.memsat_svm
  outputFilename:
    type: string?
    inputBinding:
      prefix: -o   
      position: 5

  # -f <1|2|3>     Output format for topology string.       Default: 1
  #            1 = 6-21,40-57,142-172,214-236,276-302
  #            2 = A.6,21;B.40,57;C.142,172;D.214,236;E.276,302
  #            3 = i6-21o40-57i142-172o214-236i276-302o
  # However we did not spot any differences in the output when using this flag. Not sure if it works...
  format:
    type: int?
    inputBinding:
      prefix: -f   
      position: 6
    default: 1

  mtxFile:
    type: File
    inputBinding:
      position: 7
     

outputs:
  output:
    type:
      type: array
      items: File
    outputBinding:
      glob: "*.*"


$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.22.owl



