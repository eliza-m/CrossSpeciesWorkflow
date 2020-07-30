from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys
from structural import *
from RaptorXData import *
from Scratch1dData import *
from PsiPredData import *
from DisoPredData import *

@dataclass
class StructuralPred:
    """Class that organises Structural Predictions output for single protein

    Attributes
    ----------
    DIS_threshold : float with values between 0. and 1. (default=0.50)
            Threshold used for disorder class definition of All predictors.

    ACC_threshold: probability threshold for Scratch1D (only) rellative
            solvent prediction class definition, default=0.20


    RaptorXDir : Path
        Path of the folder where RaptorX prediction output is being stored.

    PsiPredDir : Path
        Path of the folder where PsiPred prediction output is being stored.

    DisoPredDir : Path
        Path of the folder where DisoPred prediction output is being stored.

    Scratch1dDir : Path
        Path of the folder where Scratch1d prediction output is being stored.


    RaptorXPred : RaptorX object
        Contains parsed predictions output of RaptorX

    Scratch1dPred : Scratch1D object
        Contains parsed predictions output of Scratch1D

    PsiPredPred : PsiPred object
        Contains parsed predictions output of PsiPred

    DisoPredPred : DisoPred object
        Contains parsed predictions output of DisoPred


    Public Methods
    --------------
    parsestructural()
        Parses all the prediction output files and add the data inside the
        above attribute data structures.

    printSingleProtVertical( self )
        Prints all structural predictors in a vertical layout

    """

    DIS_threshold: float = 0.5
    ACC_threshold: float = 0.2

    predictions: dict = field(default_factory = dict)
    paths: dict = field(default_factory=dict)


    @staticmethod
    def parseall( paths : dict, DIS_threshold: float = None, ACC_threshold: float = None ) -> StructuralPred:
        """
        Parses all the prediction output files and add the data inside the
        above attribute data structures.
        """

        data = StructuralPred()

        data.DIS_threshold = DIS_threshold if (DIS_threshold is not None and 0.0 < DIS_threshold < 1.0) \
            else 0.50

        data.ACC_threshold = ACC_threshold if (ACC_threshold is not None and 0.0 < ACC_threshold < 1.0) \
            else 0.20

        for prot in paths:
            for predictor in paths[prot]:

                if predictor.lower() == "raptorx":
                    preddata = RaptorXData.parse( paths[prot][predictor] )
                elif predictor.lower() == "psipred":
                    preddata = PsiPredData.parse(paths[prot][predictor])
                elif predictor.lower() == "disopred":
                    preddata = DisoPredData.parse(paths[prot][predictor])
                elif predictor.lower() == "scratch1d":
                    preddata = Scratch1dData.parse(paths[prot][predictor])
                else:
                    print( "Unknown predictor key: ", predictor )
                    raise

                if prot not in data.predictions:
                    data.predictions[prot] = {}

                data.predictions[prot][predictor] = preddata

        return data


    def printSingleProtVertical( self : StructuralPred, protname: str ):

        try:

            data = self.predictions[ protname ]

            # Print header
            print("#Protname: ", protname, sep='\t')
            print("#DIS threshold: ", self.DIS_threshold, sep='\t')
            print("#ACC threshold (Scratch only): ", self.ACC_threshold, sep='\t')
            print("\n")

            print("#resid", "aa", \
                  "_", "RaptorX_SS3", "Scratch1D_SS3", "PsiPred_SS3", \
                  "_", "RaptorX_SS8", "Scratch1D_SS8", \
                  "_", "RaptorX_ACC3", "Scratch1D__ACC2", \
                  "_", "RaptorX_DIS", "DisoPred_DIS", sep='\t')

            seq = data["raptorx"].sequence
            protsize = len(seq)

            for id in range(protsize):
                print(id + 1, seq[id], \
                      "_", data["raptorx"].SS3_classes[id], data["scratch1d"].SS3_classes[id], \
                      data["psipred"].SS3_classes[id], \
                      "_", data["raptorx"].SS8_classes[id], data["scratch1d"].SS8_classes[id], \
                      "_", data["raptorx"].ACC3_classes[id], data["scratch1d"].ACC2_classes[id], \
                      "_", data["raptorx"].DIS_classes[id], data["disopred"].DIS_classes[id], sep='\t')
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
