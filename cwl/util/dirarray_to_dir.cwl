cwlVersion: v1.0
class: ExpressionTool

requirements:
  InlineJavascriptRequirement: {}

inputs:
  inputFolder: Directory[]

  outputFolder: 
    type: string?
    default: Myfolder
    doc: |
      Output directory name

outputs:
  folder: Directory

expression: |
  ${
    var folder = {
      "class": "Directory",
      "basename": inputs.outputFolder,
      "listing": inputs.inputFolder
    };
    return { "folder": folder };
  }
    
doc: |
  Merges a Directory array into a single Directory



