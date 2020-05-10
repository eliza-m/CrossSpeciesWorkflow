import sys


class RaptorXProperty:
    # default threshold value as used by RaptorX, but it can be reinterpreted
    # at parsing if one wants to
    DIS_threshold = 0.50

    def __init__(self):
        self.SS3_classes = []
        self.SS3_proba = []
        self.SS3_conf = []

        self.SS8_classes = []
        self.SS8_proba = []

        self.ACC_classes = []
        self.ACC_proba = []
        self.ACC_conf = []

        self.DIS_classes = []
        self.DIS_proba = []

        # TODO
        # self.TM2_classes = []
        # self.TM2_proba = []
        #
        # self.TM8_classes = []
        # self.TM8_proba = []


    def parseResults( self, proteinName, folderName ):
        fileNameRoot = folderName + '/' + proteinName

        self.SS3_classes, self.SS3_proba = RaptorXProperty.readSS3(  fileNameRoot + '.ss3' )
        self.SS8_classes, self.SS8_proba = RaptorXProperty.readSS8(  fileNameRoot + '.ss8' )
        self.ACC_classes, self.ACC_proba = RaptorXProperty.readACC(  fileNameRoot + '.acc' )
        self.DIS_classes, self.DIS_proba = RaptorXProperty.readDIS(  fileNameRoot + '.diso' )

        self.SS3_conf, self.ACC_conf = RaptorXProperty.readCONF(  fileNameRoot + '.tgt2' )



    def readDIS( fileName ):
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
                    if current >= RaptorXProperty.DIS_threshold:
                        DIS_classes.append( 'D' )
                    else:
                        DIS_classes.append( 'O' )

        except OSError as e:
            print(e.errno)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


        return DIS_classes, DIS_proba

    # Reads ${name}.ss3 file
    def readSS3( fileName ):
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

                    SS3_proba.append( { "H": Hproba,
                                        "E": Eproba,
                                        "C": Cproba } )
                    SS3_classes.append(ss)

        except OSError as e:
            print(e.errno)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


        return SS3_classes, SS3_proba


    # Reads ${name}.ss8 file. Classes are named as in DSSP
    def readSS8( fileName ):
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
            print(e.errno)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


        return SS8_classes, SS8_proba


    # Reads ${name}.acc file
    # classes: B (Bury, pACC: 0-10), M (Medium, pACC: 11-40) and E (Exposed,
    # pACC: 41-100).
    # TODO: add normalization feature if possible... as other define B (burried)
    # with different threshholds....
    def readACC( fileName ):
        ACC_classes = []
        ACC_proba = []

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

                    ACC_proba.append( { "B": Bproba,
                                        "M": Mproba,
                                        "E": Eproba } )
                    ACC_classes.append( acc )

        except OSError as e:
            print(e.errno)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return ACC_classes, ACC_proba


    # Reads ${name}.tgt2 file to extract confidence values (0 to 9)
    def readCONF( fileName ):
        ACC_conf = []
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
                ACC_conf.append( int( ACCconf[ it ] ) )

        except OSError as e:
            print(e.errno)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return SS3_conf, ACC_conf
