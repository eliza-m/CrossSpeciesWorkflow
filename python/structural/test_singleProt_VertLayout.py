import sys, os
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
from StructuralPred import * 


CSW_HOME = os.environ.get('CSW_HOME')

resultsfolder = CSW_HOME + "test/bash/single_protein/output/structural/"



paths = {'1pazA':
            {   'raptorx' : Path(resultsfolder + "raptorx/expected_output/"),
                'psipred' : Path(resultsfolder + "psipred/expected_output/"),
                'disopred': Path(resultsfolder + "disopred/expected_output/"),
                'scratch1d': Path(resultsfolder + "scratch1d/expected_output/")
            }
        }

pred = StructuralPred.parseall( paths)

protname = "1pazA"
pred.printSingleProtVertical(protname)

