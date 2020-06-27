import sys
# import os

class RaptorX:
    """Class that parses RaptorX-property prediction output data.

    Parameters
    ----------
    DIS_threshold: float
        probability threshold for DisPRO disorder prediction class
        definition, default=0.50

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
        Contains SS3/SS8 prediction confidence (the same values for 3 and 8
        classes as SS3 is being calculated based on SS8 classification)
        Confidence values are on a scale from 0 (least confident)
        to 9 (very confident). Please keep in mind that confidence measures
        accross different structural predictors are probably not comparable as
        they are defined differently between the methods. Please consult each
        predictor documentation and paper for further info.


    SS8_classes : array of str of size (n_aminoacis)
        Predicted Secondary structure in 8 class classification (H - alphahelix,
        G - 310 helix, I - pi helix, E - sheet, B - strand, S - bend, T - turn,
        C - coil).

    SS8_proba : array of dictionaries of size (n_aminoacis * 8 dictkeys * float)
        Stores SS8 class probability. Dictionary keys are:
            "H" - alpha helix probability (float)
            "G" - 310 helix probability (float)
            "I" - pi helix probability (float)
            "E" - sheet probability (float)
            "B" - strand probability (float)
            "T" - turn probability (float)
            "S" - bend probability (float)
            "C" - coil probability (float)
        Sum of all 8 probabilities must be ~ 1.
        For a particular residue id "resid", the alpha helix probability is:
        this.SS8_proba[ resid ][ "H" ]

    SS8_conf : empty array
        Contains SS3/SS8 prediction confidence (the same values for 3 and 8
        classes as SS3 is being calculated based on SS8 classification)
        Confidence values are on a scale from 0 (least confident)
        to 9 (very confident). Please keep in mind that confidence measures
        accross different structural predictors are probably not comparable as
        they are defined differently between the methods. Please consult each
        predictor documentation and paper for further info.



    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    TODO: add more options regarding RSA threshholds !!!!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    ACC3_classes : array of str of size (n_aminoacis)
        Predicted Relatice solvent aceessibility (RSA) in the original 3 classes
        split used by RaptorX:
        B - burried (pACC: 0-10),
        M - mediumly burried (pACC: 11-40),
        E - exposed (pACC: 41-100).
        where pACC is the relative solvent accessibility value defined by DSSP.

    ACC3_proba : array of dictionaries of size (n_aminoacis * 3 dictkeys * float)
        Stores ACC3 class probability. Dictionary keys are:
            "B" - burried probability (float)
            "M" - mediumly burried probability (float)
            "E" - exposed probability (float)
        as defined above.
        Sum of all 3 probabilities must be ~ 1.
        For a particular residue id "resid", the probability to be solvent
        exposed is:
        this.ACC3_proba[ resid ][ "E" ]

    ACC3_conf : empty array
        Contains ACC prediction confidence on a scale from 0 (least confident)
        to 9 (very confident). Please keep in mind that confidence measures
        accross different structural predictors are probably not comparable as
        they are defined differently between the methods. Please consult each
        predictor documentation and paper for further info.


    DIS_threshold : float with values between 0. and 1. (default=0.50)
        Threshold used for disorder class definition.

    DIS_classes : array of str of size (n_aminoacis)
        Predicted disordered regions in 2 classes based on
        DIS_threshold (default = 0.50) : O - ordered, D - disorder.

    DIS_proba : array of float of size (n_aminoacis * float)
        Stores disorder class probability.


    Public Methods
    --------------
    parseResults( self, proteinName, folderName )
        Parses the RaptorX prediction output files and add the data inside the
        above attribute data structures.
        Passed as arguments are the folder name folderName (according to
        raptorX provided output folder) and the protein name (ex "1pazA") that
        is being used as root for each output file (that are composed of the
        proteinName and a specific extension for each output file type
        (example: "1pazA.ss3", "1pazA.ss3_simple", "1pazA.ss8", etc).
        The proteinName string is actually the first word provided in the
        initial FASTA file header that was subjected to prediction with RaptorX.
    """


    def __init__(self, DIS_threshold = None ):
        """
        Parameters
        ----------
        DIS_threshold : float with values between 0. and 1. (default=0.50)
            Threshold used for disorder class definition.
        """

        self.DIS_threshold = DIS_threshold if ( DIS_threshold is not None and \
                                    DIS_threshold > 0.0 and \
                                    DIS_threshold < 1.0 ) \
                                    else 0.50

        self.sequence = []

        self.SS3_classes = []
        self.SS3_proba = []
        self.SS3_conf = []

        self.SS8_classes = []
        self.SS8_proba = []

        self.ACC3_classes = []
        self.ACC3_proba = []
        self.ACC3_conf = []

        self.DIS_classes = []
        self.DIS_proba = []


        # TODO
        # self.TM2_classes = []
        # self.TM2_proba = []
        #
        # self.TM8_classes = []
        # self.TM8_proba = []


    def parseResults( self, proteinName : str, folderName  : str):
        """
        Parses the RaptorX prediction output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        proteinName : str
            protein name that is being used as root for each output file.
            (example: "1paz.ss3", "1paz.ss3_simple", "1paz.ss8", etc).

        folderName : str
            folder name where RaptorX prediction output is being stored.
            (example: "CrossSpeciesWorkflow/output/1pazA/RaptorX/1pazA_PROP/")
        """

        fileNameRoot = folderName + '/' + proteinName


        self.sequence, self.SS3_classes, self.SS3_proba = \
            RaptorX.__readSS3( fileNameRoot + '.ss3' )
        self.SS8_classes, self.SS8_proba = \
            RaptorX.__readSS8(  fileNameRoot + '.ss8' )
        self.ACC3_classes, self.ACC3_proba = \
            RaptorX.__readACC(  fileNameRoot + '.acc' )
        self.DIS_classes, self.DIS_proba = \
            RaptorX.__readDIS( fileNameRoot + '.diso', \
                                        self.DIS_threshold )

        self.SS3_conf, self.ACC3_conf = \
            RaptorX.__readCONF( fileNameRoot + '.tgt2')



    def __readDIS( fileName : str, DIS_threshold  : float):
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
        DIS_classes = []
        DIS_proba = []

        try:
            f = open(fileName, 'r')
            lines = f.readlines()
            for line in lines:
                l = line.split()
                if l[0][0] != '#':
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


        return DIS_classes, DIS_proba


    def __readSS3( fileName : str):
        """
        Parses "*.ss3" output files and add the data inside the
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
                if l[0][0] != '#':

                    Hproba = float(l[3])
                    Eproba = float(l[4])
                    Cproba = float(l[5])
                    ss = l[2]

                    seq.append(l[1])
                    SS3_proba.append( { "H": Hproba,
                                        "E": Eproba,
                                        "C": Cproba } )
                    SS3_classes.append(ss)

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


        return seq, SS3_classes, SS3_proba


    def __readSS8( fileName : str ):
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
        SS8_proba = []

        try:
            f = open(fileName, 'r')
            lines = f.readlines()
            for line in lines:
                l = line.split()
                if l[0][0] != '#':
                    Hproba = float(l[3])
                    Gproba = float(l[4])
                    Iproba = float(l[5])
                    Eproba = float(l[6])
                    Bproba = float(l[7])
                    Tproba = float(l[8])
                    Sproba = float(l[9])
                    Cproba = float(l[10])

                    ss = l[2]


                    SS8_proba.append( { "H": Hproba,
                                        "G": Gproba,
                                        "I": Iproba,
                                        "E": Eproba,
                                        "B": Bproba,
                                        "T": Tproba,
                                        "S": Sproba,
                                        "C": Cproba    } )

                    if ss == 'L':
                        ss = 'C'

                    SS8_classes.append(ss)

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


        return SS8_classes, SS8_proba



    def __readACC( fileName : str ):
        """
        Parses "*.acc" output files and add the data inside the
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
        ACC3_classes = []
        ACC3_proba = []

        try:
            f = open(fileName, 'r')
            lines = f.readlines()
            for line in lines:
                l = line.split()
                if l[0][0] != '#':
                    Bproba = float(l[3])
                    Mproba = float(l[4])
                    Eproba = float(l[5])

                    acc = l[2]

                    ACC3_proba.append( { "B": Bproba,
                                        "M": Mproba,
                                        "E": Eproba } )
                    ACC3_classes.append( acc )

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return ACC3_classes, ACC3_proba


    def __readCONF( fileName : str ):
        """
        Parses "*.tgt2" output files and add the data inside the
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
        ACC3_conf = []
        SS3_conf = []

        try:
            f = open(fileName, 'r')
            lines = f.readlines()
            for line in lines:
                l = line.split()
                if len(l) > 2 and l[0] == 'SSEconf':
                    SS3conf = l[2]
                if len(l) > 2 and l[0] == 'ACCconf':
                    ACCconf = l[2]

            for it in range(len(SS3conf)):
                SS3_conf.append( int( SS3conf[ it ] ) )
                ACC3_conf.append( int( ACCconf[ it ] ) )

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return SS3_conf, ACC3_conf



#
#
# CSW_HOME = os.environ.get('CSW_HOME')
# predData = RaptorX()
# proteinName = "1pazA"
# folderName = CSW_HOME + "/output/1pazA/RaptorX/1pazA_PROP/"
#
# predData.parseResults( proteinName, folderName )
