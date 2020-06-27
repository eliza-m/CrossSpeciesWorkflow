import sys
# import os

from StructuralPredictions import *
from parsers import *


# CSW_HOME = os.environ.get('CrossSpeciesWorkflow_HOME')
# proteinName = "1pazA"
# resultsFolder = CSW_HOME + "/output/1pazA/"

# the provided example in input & output folders
proteinName = sys.argv[1]
resultsFolder = sys.argv[2]

pred = StructuralPredictions(proteinName, resultsFolder)

# parsing all predictors outputs
pred.parseAllResults()

pred.printSingleProtVertical()
