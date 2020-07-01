import sys
from parsers.RaptorX import *
from parsers.Scratch1D import *
from parsers.PsiPred import *
from parsers.DisoPred import *


class StructuralPredictions:
    """Class that organises Structural Predictions output

    Parameters
    ----------
    DIS_threshold : float with values between 0. and 1. (default=0.50)
            Threshold used for disorder class definition of All predictors.

    ACC_threshold: probability threshold for Scratch1D (only) rellative
            solvent prediction class definition, default=0.20


    proteinName : str
            protein name that is being used as root for each output file.
            By default it is the root name of the FASTA file.
            (example: "1pazA" for "1pazA.fasta" file used as example).

    outputFolder : str
            Path of the folder where all prediction output is being stored.
            (example: "${CrossSpeciesWorkflow_HOME}/output/1pazA/")


    Attributes
    ----------

    RaptorXpred : RaptorX object
        Contains parsed predictions output of RaptorX

    Scratch1Dpred : Scratch1D object
        Contains parsed predictions output of Scratch1D

    PsiPredpred : PsiPred object
        Contains parsed predictions output of PsiPred

    DisoPredpred : DisoPred object
        Contains parsed predictions output of DisoPred


    Public Methods
    --------------
    parseAllResults( self )
        Parses all the prediction output files and add the data inside the
        above attribute data structures.

    printSingleProtVertical( self )
        Prints all structural predictors in a vertical layout

    """

    def __init__(self, proteinName : str , outputFolder : str, \
                DIS_threshold = None, ACC_threshold = None ):
        """
        Parameters
        ----------
        DIS_threshold : float with values between 0. and 1. (default=0.50)
            Threshold used for disorder class definition of All predictors.

        ACC_threshold: probability threshold for Scratch1D (only) rellative
            solvent prediction class definition, default=0.20

        proteinName : str
            protein name that is being used as root for each output file.
            By default it is the root name of the FASTA file.
            (example: "1pazA" for "1pazA.fasta" file used as example).

        outputFolder : str
            Path of the folder where all prediction output is being stored.
            (example: "${CrossSpeciesWorkflow_HOME}/output/1pazA/")

        """

        self.DIS_threshold = DIS_threshold if ( DIS_threshold is not None and \
                                    DIS_threshold > 0.0 and \
                                    DIS_threshold < 1.0 ) \
                                    else 0.50

        self.ACC_threshold = ACC_threshold if ( ACC_threshold is not None and \
                                    ACC_threshold > 0.0 and \
                                    ACC_threshold < 1.0 ) \
                                    else 0.20

        self.RaptorXOutput = RaptorX( self.DIS_threshold )
        self.Scratch1DOutput = Scratch1D( self.DIS_threshold, self.ACC_threshold )
        self.PsiPredOutput = PsiPred()
        self.DisoPredOutput = DisoPred( self.DIS_threshold )

        self.proteinName = proteinName
        self.outputFolder = outputFolder



    def parseAllResults( self ):
        """
        Parses all the prediction output files and add the data inside the
        above attribute data structures.
        """

        # RaptorX
        RaptorXfileNameRoot = self.outputFolder + '/RaptorX/' + self.proteinName + '_PROP/'
        self.RaptorXOutput.parseResults( self.proteinName, RaptorXfileNameRoot )

        # Scratch1D
        Scratch1DfileNameRoot = self.outputFolder + '/Scratch1D/'
        self.Scratch1DOutput.parseResults( self.proteinName, Scratch1DfileNameRoot )

        # PsiOutput
        PsiPredfileNameRoot = self.outputFolder + '/PsiPred/'
        self.PsiPredOutput.parseResults( self.proteinName, PsiPredfileNameRoot )

        # Disopred
        DisoPredfileNameRoot = self.outputFolder + '/DisoPred/'
        self.DisoPredOutput.parseResults( self.proteinName, DisoPredfileNameRoot )



    def printSingleProtVertical( self ):

        # Print header
        print("#Protname: ", self.proteinName, sep='\t')
        print("#OutputFolder: ", self.outputFolder, sep='\t')
        print("#DIS threshold: ", self.DIS_threshold, sep='\t')
        print("#ACC threshold (Scratch only): ", self.ACC_threshold, sep='\t')
        print("\n")

        print("#resid", "aa", \
            "_", "RaptorX_SS3", "Scratch1D_SS3", "PsiPred_SS3", \
            "_", "RaptorX_SS8", "Scratch1D_SS8", \
            "_", "RaptorX_ACC3", "Scratch1D__ACC2", \
            "_", "RaptorX_DIS", "DisoPred_DIS", sep='\t')

        seq = self.RaptorXOutput.sequence
        protsize = len(seq)

        for id in range(protsize):
            print( id + 1, seq[id], \
            "_", self.RaptorXOutput.SS3_classes[id], self.Scratch1DOutput.SS3_classes[id], self.PsiPredOutput.SS3_classes[id], \
            "_", self.RaptorXOutput.SS8_classes[id], self.Scratch1DOutput.SS8_classes[id], \
            "_", self.RaptorXOutput.ACC3_classes[id], self.Scratch1DOutput.ACC2_classes[id], \
            "_", self.RaptorXOutput.DIS_classes[id], self.DisoPredOutput.DIS_classes[id], sep='\t' )
