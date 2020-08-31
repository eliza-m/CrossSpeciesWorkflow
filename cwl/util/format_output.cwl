#!/usr/bin/env cwl-runner


cwlVersion: v1.0
class: CommandLineTool
baseCommand: [format-output]
hints:
  DockerRequirement:
    dockerPull: quay.io/dbsb-ibar/species_proteins:latest


requirements:
  InlineJavascriptRequirement: {}


inputs:

# Required inputs:

  formattype:
    type: 
      - "null"
      - type: enum
        symbols:
          - single  # single protein format
          - multi   # multiple proteins aligned
    inputBinding:
      prefix: --format
    doc: |
      Layout type of the output file.

  module:
    type: 
      - "null"
      - type: enum
        symbols:
          - all                  # all modules
          - ptm                  # Post translation modifications : glyco + acety + sumo + lipid
          - struct               # Structural module only
          - glyc                 # Glycosylation module only
          - phos                 # Phosphorylation module only
          - acet                 # Acetylation module only
          - lipid                # Lipid module only
          - sumo                 # SUMOylation module only
          - loc                  # Cellular Localisation module only
    inputBinding:
      prefix: --module
    doc: |
      Individual module or group of modules to be parsed and merged into the output file.

  inputFolder:
    type: Directory
    inputBinding:
      prefix: --inputfolder
    doc: |
      Folder where all prediction output are stored. It also needs to contain the protein(s) fasta file.

  alnFile:
    type: File?
    inputBinding:
      prefix: --alnfile
    doc: |
      Alignment file


# Optional inputs:

  signif:
    type: boolean?
    inputBinding:
      prefix: --signif
    default: False
    doc: |
      print only significant predicted sites. Significance thresholds are predictor specific

  outputFilename:
    type: string?
    inputBinding:
      prefix: --output
    default: "results.txt"
    doc: |
      output filename of the parsed data


  protname:
    type: string?
    inputBinding:
      prefix: --protname
    default: null
    doc: |
      Only for 'single' protein layout. It is advisable to provide a basename
      for filenames, especially when, within the specified input folder there
      are none or multiple files with the same extensions.
      Providing a baseroot name (ex: 'LEUK_RAT'), will help dealing
      with potential confusions and files such as $protname.$predictor*
      will be searched instead.
      If protname is not provided, *.$predictor* files will be searched.
      In case of ambiguities ( none or multiple files with same extensios)
      an error is raised.



outputs:
  output:
    type: File
    outputBinding:
      glob: '*'
      outputEval: |
        ${
          if ( inputs.outputFilename != "results.txt"){
             self[0].basename =  inputs.outputFilename;
          }
          else if (inputs.protname != null) {
             self[0].basename = inputs.protname + "." + inputs.formattype + "." + inputs.module + ".out";
          }
          else{
             self[0].basename = inputs.module + "_results.txt";
          }
          return self[0]
        }

doc: |
  Parses and merge all predictors outputs in a nice formatted output file
  It offers various output formatting options, such as parsing results only
  for a specific module or a combination of modules, and different layouts
  depending on whether there are prediction results only for a single protein
  sequence, or a group of sequencing that needs to be aligned.
  Additional options include whether to print all predicted sites data,
  or only significant ones depending on each predictors's thresholds



