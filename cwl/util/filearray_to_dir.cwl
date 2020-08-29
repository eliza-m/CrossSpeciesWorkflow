cwlVersion: v1.0
class: ExpressionTool

requirements:
  InlineJavascriptRequirement: {}

inputs:
  files: File[]
  foldername: 
    type: string?
    default: Myfolder

outputs:
  folder: Directory

expression: |
  ${
  return {"folder": {"class": "Directory", "basename": inputs.foldername, "listing": inputs.files}};
  }