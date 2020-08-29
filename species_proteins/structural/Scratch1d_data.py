from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys


@dataclass
class Scratch1d_data:
    """Class that parses Baldi's group -  Scratch1D prediction output
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

    ACC_threshold: probability threshold for Scratch1D relative solvent
        prediction class definition, default=0.20

    ACC2_classes : array of str of size (n_aminoacis)
        Predicted Relative solvent accessibility (RSA) in 2 classes based on
        ACC_threshold (default = 0.20) : B - buried, E - exposed.


    Public Methods
    --------------
    parse ( folder : Path, ACC_threshold: float ) -> Scratch1d_data
        Parses the prediction output files and add the data inside the above attribute data structures. Passed
        as arguments are the folder name (the scratch1D output folder).

    parse_files(ss: Path, ss8: Path, acc20: Path, ACC_threshold: float) -> Scratch1d_data:
        Parses the prediction output files and add the data inside the above attribute data structures. Passed
        as arguments are the files paths.
    """

    SS3_classes: list
    SS8_classes: list
    ACC2_classes: list
    ACC_threshold: float = 0.2

    @staticmethod
    def parse_files(ss: Path, ss8: Path, acc20: Path, ACC_threshold: float = None) -> Scratch1d_data:
        """
        Parses the prediction output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        ss : path to *.ss file
        ss8 : path to *.ss8 file
        acc20 : path to *.acc file
        ACC_threshold: probability threshold for Scratch1D relative solvent
            prediction class definition, default=0.20

        Returns:
        -------
        Scratch1d_data: with parsed data
        """

        ACC_threshold = ACC_threshold if (ACC_threshold is not None and 0.0 < ACC_threshold < 1.0) else 0.20

        SS3_classes = Scratch1d_data.__readss(ss)
        SS8_classes = Scratch1d_data.__readss(ss8)
        ACC2_classes = Scratch1d_data.__readacc(acc20, ACC_threshold)

        return Scratch1d_data( SS3_classes=SS3_classes, SS8_classes=SS8_classes, ACC2_classes=ACC2_classes  )

    @staticmethod
    def parse(folder: Path, ACC_threshold: float = None) -> Scratch1d_data:
        """
         Parses the  prediction output files and add the data inside the
         above attribute data structures.

         Parameters
         ----------
         folder : Path
            Path to the folder where prediction data is generated
         ACC_threshold : float
            With values between 0. and 1. (default=0.20). Threshold used for RSA class definition.

         Returns:
         -------
         Scratch1d_data: with parsed data
         """

        ACC_threshold = ACC_threshold if (ACC_threshold is not None and 0.0 < ACC_threshold < 1.0) else 0.20

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

        return Scratch1d_data.parse_files( paths['ss'], paths['ss8'], paths['acc20'],ACC_threshold)


    @staticmethod
    def __readss( file : Path ) -> list:
        """
        Parses "*.ss" & "*.ss8" output files

        Parameters
        ----------
        file : Path

        Raises
        ------
        OSError
        Other errors

        Returns
        ------
        SS_classes : list
            Intermediary lists containing parsed data
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
    def __readacc( file : Path, ACC_threshold : float) -> list:
        """
        Parses "*.acc20" output files

        Parameters
        ----------
        file : Path
        ACC_threshold : float

        Raises
        ------
        OSError
        Other errors

        Returns
        ------
        ACC2_classes : list
            Intermediary lists containing parsed data
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



