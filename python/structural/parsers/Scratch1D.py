import sys
# import os


class Scratch1D:
    """Class that parses Baldi's group -  Scratch1D & DisPRO prediction output
    data.

    Parameters
    ----------
    DIS_threshold: probability threshold for DisPRO disorder prediction class
        definition, default=0.50

    ACC_threshold: probability threshold for Scratch1D rellative solvent
        prediction class definition, default=0.20


    Attributes
    ----------

    SS3_classes : array of str of size (n_aminoacis)
        Predicted Secondary structure in 3 class classification (H - helix,
        E - sheet, C - coil).

    SS8_classes : array of str of size (n_aminoacis)
        Predicted Secondary structure in 8 class classification (H - alphahelix,
        G - 310 helix, I - pi helix, E - sheet, B - strand, S - bend, T - turn,
        C - coil).




    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    TODO: add more options regarding RSA threshholds !!!!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    ACC_threshold: probability threshold for Scratch1D rellative solvent
        prediction class definition, default=0.20

    ACC2_classes : array of str of size (n_aminoacis)
        Predicted Relatice solvent aceessibility (RSA) in 2 classes based on
        ACC_threshold (default = 0.20) : B - burried, E - exposed.

    ACC2_values : empty array
        Predicted ACC values.


    DIS_threshold : float with values between 0. and 1. (default=0.50)
        Threshold used for disorder class definition.

    DIS_classes : array of str of size (n_aminoacis)
        Predicted disordered regions in 2 classes based on
        DIS_threshold (default = 0.50) : O - ordered, D - disorder.

    DIS_proba : empty array
        This was added only for maintaining consistency with other structural
        predictors classes, as Scratch1D does not provide the class
        probabilities


    Public Methods
    --------------
    parseResults( self, proteinName, folderName )
        Parses the prediction output files and add the data inside the
        above attribute data structures.
        Passed as arguments are the folder name folderName (according to
        Scratch1D provided output folder) and the protein name (ex "1paz") that
        is being used as root for each output file (that are composed of the
        proteinName and a specific extension for each output file type
        (example: "1paz.ss", "1paz.acc", "1paz.ss8", etc).
    """


    def __init__(self, DIS_threshold = None, ACC_threshold = None):
        """
        Parameters
        ----------
        DIS_threshold : float with values between 0. and 1. (default=0.50)
            Threshold used for disorder class definition.

        ACC_threshold: probability threshold for Scratch1D rellative solvent
            prediction class definition, default=0.20
        """

        self.DIS_threshold = DIS_threshold if ( DIS_threshold is not None and \
                                    DIS_threshold > 0.0 and \
                                    DIS_threshold < 1.0 ) \
                                    else 0.50

        self.ACC_threshold = ACC_threshold if ( ACC_threshold is not None and \
                                    ACC_threshold > 0.0 and \
                                    ACC_threshold < 1.0 ) \
                                    else 0.20

        self.SS3_classes = []
        self.SS8_classes = []

        self.ACC2_classes = []

        self.DIS_classes = []
        self.DIS_proba = []


    def parseResults( self, proteinName, folderName ):
        """
        Parses the Scratch1D prediction output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        proteinName : str
            protein name that is being used as root for each output file.
            (example: "1paz.ss3", "1paz.ss3_simple", "1paz.ss8", etc).

        folderName : str
            folder full path where Scratch1D prediction output is being stored.
            (example: "[]...]CrossSpeciesWorkflow/output/1pazA/Scratch1D/")
        """

        fileNameRoot = folderName + '/' + proteinName

        self.SS3_classes = Scratch1D.__readSS3( fileNameRoot + '.ss' )
        self.SS8_classes = Scratch1D.__readSS8(  fileNameRoot + '.ss8' )
        self.ACC2_classes = Scratch1D.__readACC( fileNameRoot + '.acc20', self.ACC_threshold )

        # self.DIS_classes, self.DIS_proba = \
        #     Scratch1D.__readDIS( fileNameRoot + '.diso', \
        #                                 self.DIS_threshold )





    def __readSS3( fileName ):
        """
        Parses "*.ss" output files and add the data inside the
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
        SS3_classes = []

        try:
            f = open(fileName, 'r')
            lines = f.readlines()
            ssLine = lines[1][:-1];
            for ss in ssLine:
                SS3_classes.append(ss)

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return SS3_classes


    def __readSS8( fileName ):
        """
        Parses "*.ss8" output files and add the data inside the
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
        SS8_classes = []

        try:
            f = open(fileName, 'r')
            lines = f.readlines()
            ssLine = lines[1][:-1];
            for ss in ssLine:
                SS8_classes.append(ss)

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return SS8_classes


    def __readACC( fileName, ACC_threshold ):
        """
        Parses "*.acc20" output files and add the data inside the
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

        ACC2_classes = []

        try:
            f = open(fileName, 'r')
            accLine = f.readlines()[1]

            accPred = accLine.split()
            for acc in accPred:

                if float(acc) <= ACC_threshold  :
                    ACC2_classes.append( "B" )
                else:
                    ACC2_classes.append( "E" )

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return ACC2_classes



    # def __readDIS( fileName, DIS_threshold ):
    #     """
    #     Parses "*.diso" output files and add the data inside the
    #     above attribute data structures.
    #
    #     Parameters
    #     ----------
    #     fileName : str
    #         Path to file
    #
    #     DIS_threshold : float
    #         Threshold for disorder class definition
    #
    #     Raises
    #     ------
    #     OSError
    #     Other errors
    #     """
    #
    #     # for cases when the method is called twice
    #     DIS_classes = []
    #     DIS_proba = []
    #
    #     try:
    #         f = open(fileName, 'r')
    #         lines = f.readlines()
    #         for line in lines:
    #             l = line.split()
    #             if l[0][0] != '#':
    #                 current = float(l[3])
    #                 DIS_proba.append( current )
    #                 if current >= DIS_threshold:
    #                     DIS_classes.append( 'D' )
    #                 else:
    #                     DIS_classes.append( 'O' )
    #
    #     except OSError:
    #         print("File error:", sys.exc_info()[0])
    #         raise
    #
    #     except:
    #         print("Unexpected error:", sys.exc_info()[0])
    #         raise
    #
    #
    #     return DIS_classes, DIS_proba


#
#
# CSW_HOME = os.environ.get('CSW_HOME')
# predData = Scratch1D()
# proteinName = "1pazA"
# folderName = CSW_HOME + "/output/1pazA/Scratch1D/"
#
# predData.parseResults( proteinName, folderName )
#
