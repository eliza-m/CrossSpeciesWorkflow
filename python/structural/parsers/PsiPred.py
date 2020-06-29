import sys
# import os

class PsiPred:
    """Class that parses PsiPred prediction output data.

    Parameters
    ----------


    Attributes
    ----------
    sequence : array of str of size (n_aminoacis)
        Amino acid sequence

    SS3_classes : array of str of size (n_aminoacis)
        Predicted Secondary structure in 3 class classification (H - helix,
        E - sheet, C - coil).

    SS3_proba : array of dictionaries of size (n_aminoacis * 3 dictkeys * float)
        Stores SS3 class probability. Dictionary keys are:
            "H" - helix probability (float)
            "E" - sheet probability (float)
            "C" - coil probability (float)
        Sum of all three H, E and C probabilities must be ~ 1.
        For a particular residue id "resid", the helix probability will be:
        this.SS3_proba[ resid ][ "H" ]

    SS3_conf : array of int of size (n_aminoacis)
        Contains SS3 prediction confidence on a scale from 0 (least confident)
        to 9 (very confident). Please keep in mind that confidence measures
        accross different structural predictors are probably not comparable as
        they are defined differently between the methods. Please consult each
        predictor documentation and paper for further info.

    Public Methods
    --------------
    parseResults( self, proteinName, folderName )
        Parses the PsiPred prediction output files and add the data inside the
        above attribute data structures.
        Passed as arguments are the folder name folderName (according to
        PsiPred provided output folder) and the protein name (ex "1pazA") that
        is being used as root for each output file (that are composed of the
        proteinName and a specific extension for each output file type
        (example: "1pazA.ss2", "1pazA.horiz", etc).
    """


    def __init__(self):

        self.sequence = []
        self.SS3_classes = []
        self.SS3_proba = []
        self.SS3_conf = []


    def parseResults( self, proteinName : str, folderName : str ):
        """
        Parses the PsiPred prediction output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        proteinName : str
            protein name that is being used as root for each output file.
            (example: "1paz.ss3", "1paz.ss3_simple", "1paz.ss8", etc).

        folderName : str
            folder name where PsiPred prediction output is being stored.
            (example: "CrossSpeciesWorkflow/output/1pazA/PsiPred/")
        """

        fileNameRoot = folderName + '/' + proteinName

        self.sequence, self.SS3_classes, self.SS3_proba = \
            PsiPred.__readSS3( fileNameRoot + '.ss2' )

        self.SS3_conf = \
            PsiPred.__readCONF( fileNameRoot + '.horiz')



    def __readSS3( fileName : str ) :
        """
        Parses "*.ss2" output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        fileName : str
            Path to file

        Raises
        ------
        OSError
        Other errors
        """

        # for cases when the method is called twice
        seq = []
        SS3_classes = []
        SS3_proba = []

        try:
            f = open(fileName, 'r')
            lines = f.readlines()
            for line in lines:
                l = line.split()
                if len(l) > 1 and l[0][0] != '#' :
                    Cproba = float(l[3])
                    Hproba = float(l[4])
                    Eproba = float(l[5])
                    ss = l[2]

                    SS3_proba.append( { "H": Hproba,
                                        "E": Eproba,
                                        "C": Cproba } )
                    SS3_classes.append(ss)
                    seq.append(l[1])

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


        return seq, SS3_classes, SS3_proba


    def __readCONF( fileName : str)  :
        """
        Parses "*.horiz" output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        fileName : str
            Path to file

        Raises
        ------
        OSError
        Other errors
        """

        # for cases when the method is called twice
        SS3_conf = []

        try:
            f = open(fileName, 'r')
            lines = f.readlines()
            for line in lines:
                l = line.split()
                if len(l) > 1 and l[0] == 'Conf:':
                    SS3conf = l[1]
                    for it in range(len(SS3conf)):
                        SS3_conf.append( int( SS3conf[ it ] ) )


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return SS3_conf



#
#
# CSW_HOME = os.environ.get('CSW_HOME')
# predData = PsiPred()
# proteinName = "1pazA"
# folderName = CSW_HOME + "/output/1pazA/PsiPred/"
#
# predData.parseResults( proteinName, folderName )
