from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys


@dataclass
class Scratch1dData:
    """Class that parses Baldi's group -  Scratch1D & DisPRO prediction output
    data.

    Attributes
    ----------

    SS3_classes : array of str of size (n_aminoacis)
        Predicted Secondary structure in 3 class classification (H - helix,
        E - sheet, C - coil).

    SS8_classes : array of str of size (n_aminoacis)
        Predicted Secondary structure in 8 class classification (H - alphahelix,
        G - 310 helix, I - pi helix, E - sheet, B - strand, S - bend, T - turn,
        C - coil).


    ACC_threshold: probability threshold for Scratch1D rellative solvent
        prediction class definition, default=0.20

    ACC2_classes : array of str of size (n_aminoacis)
        Predicted Relatice solvent aceessibility (RSA) in 2 classes based on
        ACC_threshold (default = 0.20) : B - burried, E - exposed.


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
    parse ( folder : Path, DIS_threshold: float, ACC_threshold: float ) -> Scratch1dData
        Parses the prediction output files and add the data inside the above attribute data structures. Passed
        as arguments are the folder name (the scratch1D output folder).

    parsefiles(ss: Path, ss8: Path, acc20: Path, DIS_threshold: float, ACC_threshold: float) -> Scratch1dData:
        Parses the prediction output files and add the data inside the above attribute data structures. Passed
        as arguments are the files paths.
    """


    DIS_threshold: float = 0.5
    ACC_threshold: float = 0.2

    sequence: list = field(default_factory = list)

    SS3_classes: list = field(default_factory = list)
    SS8_classes: list = field(default_factory = list)

    ACC2_classes: list = field(default_factory = list)

    DIS_classes: list = field(default_factory = list)
    DIS_proba: list = field(default_factory = list)



    @staticmethod
    def parsefiles(ss: Path, ss8: Path, acc20: Path, DIS_threshold: float = None, ACC_threshold: float = None) -> Scratch1dData:
        """
        Parses the RaptorX prediction output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        ss : path to *.ss file
        ss8 : path to *.ss8 file
        acc20 : path to *.acc file

        DIS_threshold : float with values between 0. and 1. (default=0.50)
            Threshold used for disorder class definition.

        ACC_threshold: probability threshold for Scratch1D rellative solvent
            prediction class definition, default=0.20

        Returns:
        -------
        Scratch1dData: with parsed data
        """

        data = Scratch1dData()

        data.DIS_threshold = DIS_threshold if (DIS_threshold is not None and 0.0 < DIS_threshold < 1.0) \
            else 0.50
        data.ACC_threshold = ACC_threshold if (ACC_threshold is not None and 0.0 < ACC_threshold < 1.0) \
            else 0.20

        data.SS3_classes = data.__readss(ss)
        data.SS8_classes = data.__readss(ss8)
        data.ACC2_classes = data.__readacc(acc20, data.ACC_threshold)

        return data

    @staticmethod
    def parse(folder: Path, DIS_threshold: float = None, ACC_threshold: float = None) -> Scratch1dData:
        """
         Parses the  prediction output files and add the data inside the
         above attribute data structures.

         Parameters
         ----------
         folder : Path
            Path to the folder where prediction data is generated

         DIS_threshold : float
            With values between 0. and 1. (default=0.50). Threshold used for disorder class definition.

         ACC_threshold : float
            With values between 0. and 1. (default=0.20). Threshold used for RSA class definition.

         Returns:
         -------
         Scratch1dData: with parsed data
         """

        data = Scratch1dData()

        data.DIS_threshold = DIS_threshold if (DIS_threshold is not None and 0.0 < DIS_threshold < 1.0) \
            else 0.50

        data.ACC_threshold = ACC_threshold if (ACC_threshold is not None and 0.0 < ACC_threshold < 1.0) \
            else 0.20

        paths = { 'ss' : Path(),
                    'ss8' : Path(),
                    'acc20' : Path()
                    }

        for key in paths :
            try:
                files = list(folder.rglob('*.' + key))
                if len(files) > 1:
                    print("Multiple options: ", list)
                    raise
                elif len(files) == 0:
                    print("In the folder there is no file with suffix : ", key)
                    raise
                else:
                    paths[key] = files[0]

            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

        data = data.parsefiles( paths['ss'], paths['ss8'], paths['acc20'], data.DIS_threshold, data.ACC_threshold)

        return data


    @staticmethod
    def __readss( file : Path ):
        """
        Parses "*.ss" & "*.ss8" output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        file : Path

        Raises
        ------
        OSError
        Other errors
        """

        SS_classes = []

        try:
            f = open(file, 'r')
            lines = f.readlines()
            ssLine = lines[1][:-1];
            for ss in ssLine:
                SS_classes.append(ss)

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return SS_classes


    @staticmethod
    def __readacc( file : Path, ACC_threshold : float):
        """
        Parses "*.acc20" output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        file : Path
        ACC_threshold : float

        Raises
        ------
        OSError
        Other errors
        """

        ACC2_classes = []

        try:
            f = open(file, 'r')
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


