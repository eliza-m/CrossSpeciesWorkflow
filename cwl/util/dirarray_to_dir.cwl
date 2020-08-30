cwlVersion: v1.0
class: ExpressionTool

requirements:
  InlineJavascriptRequirement: {}

inputs:
  inputFolder: Directory[]
  outputFolder: 
    type: string?
    default: Myfolder

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
  Organize all prediction output as a single folder, that will become next step's input



