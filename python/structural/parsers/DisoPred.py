import sys
# import os

class DisoPred:
    """Class that parses DisoPred prediction output data.

    Parameters
    ----------
    DIS_threshold: float
        probability threshold for DisPRO disorder prediction class
        definition, default=0.50

    Attributes
    ----------
    sequence : array of str of size (n_aminoacis)
        Amino acid sequence

    DIS_classes : array of str of size (n_aminoacis)
        Predicted disordered regions in 2 classes based on
        DIS_threshold (default = 0.50) : O - ordered, D - disorder.

    DIS_proba : array of float of size (n_aminoacis * float)
        Stores disorder class probability.

    Public Methods
    --------------
    parseResults( self, proteinName, folderName )
        Parses the DisoPred prediction output files and add the data inside the
        above attribute data structures.
        Passed as arguments are the folder name folderName (according to
        DisoPred provided output folder) and the protein name (ex "1pazA") that
        is being used as root for each output file (that are composed of the
        proteinName and a specific extension for each output file type
        (example: "1pazA.diso").
    """


    def __init__(self, DIS_threshold = None):
        """
        Parameters
        ----------
        DIS_threshold : float with values between 0. and 1. (default=0.50)
            Threshold used for disorder class definition.
        """

        self.sequence = []
        self.DIS_threshold = DIS_threshold if ( DIS_threshold is not None and \
                                    DIS_threshold > 0.0 and \
                                    DIS_threshold < 1.0 ) \
                                    else 0.50
        self.DIS_classes = []
        self.DIS_proba = []



    def parseResults( self, proteinName : str, folderName : str ):
        """
        Parses the DisoPred prediction output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        proteinName : str
            protein name that is being used as root for each output file.
            (example: "1paz.ss3", "1paz.ss3_simple", "1paz.ss8", etc).

        folderName : str
            folder name where DisoPred prediction output is being stored.
            (example: "CrossSpeciesWorkflow/output/1pazA/DisoPred/")
        """

        fileNameRoot = folderName + '/' + proteinName

        self.sequence, self.DIS_classes, self.DIS_proba = \
            DisoPred.__readDIS( fileNameRoot + '.diso', self.DIS_threshold )



    def __readDIS( fileName, DIS_threshold : float):
        """
        Parses "*.diso" output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        fileName : str
            Path to file

        DIS_threshold : float
            Threshold for disorder class definition

        Raises
        ------
        OSError
        Other errors
        """

        # for cases when the method is called twice
        seq = []
        DIS_classes = []
        DIS_proba = []

        try:
            f = open(fileName, 'r')
            lines = f.readlines()
            for line in lines:
                l = line.split()
                if l[0][0] != '#':
                    seq.append(l[1])
                    current = float(l[3])
                    DIS_proba.append( current )
                    if current >= DIS_threshold:
                        DIS_classes.append( 'D' )
                    else:
                        DIS_classes.append( 'O' )

        except OSError:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


        return seq, DIS_classes, DIS_proba

#
#
# CSW_HOME = os.environ.get('CSW_HOME')
# predData = DisoPred()
# proteinName = "1pazA"
# folderName = CSW_HOME + "/output/1pazA/DisoPred/"
#
# predData.parseResults( proteinName, folderName )
