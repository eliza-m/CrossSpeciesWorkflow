cwlVersion: v1.0
class: ExpressionTool

requirements:
  InlineJavascriptRequirement: {}

inputs:
  files: File[]
    doc: |
      Input file array

  foldername: 
    type: string?
    default: Myfolder
    doc: |
      Output directory name

outputs:
  folder: Directory

expression: |
  ${
  return {"folder": {"class": "Directory", "basename": inputs.foldername, "listing": inputs.files}};
  }

doc: |
  Merges a File array into a single Directory