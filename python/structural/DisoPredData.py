from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys

@dataclass
class DisoPredData:
    """Class that parses DisoPred prediction output data.

    Attributes
    ----------
    DIS_threshold: float
        probability threshold for DisPRO disorder prediction class
        definition, default=0.50

    sequence : array of str of size (n_aminoacis)
        Amino acid sequence

    DIS_classes : array of str of size (n_aminoacis)
        Predicted disordered regions in 2 classes based on
        DIS_threshold (default = 0.50) : O - ordered, D - disorder.

    DIS_proba : array of float of size (n_aminoacis * float)
        Stores disorder class probability.


    Public Methods
    --------------
    parse ( folder : Path, DIS_threshold: float ) -> DisoPredData
        Parses the prediction output files and add the data inside the above attribute data structures. Passed
        as arguments are the folder name (according to prediction output folder) and optionally a threshold for
        disorder.

    parsefiles( diso: Path, DIS_threshold=None) -> DisoPredData:
        Parses the prediction output files and add the data inside the above attribute data structures. Passed
        as arguments are the files paths and optionally a threshold for disorder.
    """


    DIS_threshold: float = 0.5

    sequence: list = field(default_factory = list)

    DIS_classes: list = field(default_factory = list)
    DIS_proba: list = field(default_factory = list)


    @staticmethod
    def parsefiles(diso: Path, DIS_threshold=None) -> DisoPredData:
        """
        Parses the prediction output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        diso : path to *.diso file
        DIS_threshold : float with values between 0. and 1. (default=0.50)
            Threshold used for disorder class definition.

        Returns:
        -------
        DisoPredData: with parsed data
        """

        data = DisoPredData()
        data.DIS_threshold = DIS_threshold if (DIS_threshold is not None and 0.0 < DIS_threshold < 1.0) \
            else 0.50

        data.sequence, data.DIS_classes, data.DIS_proba = data.__readdiso(diso, data.DIS_threshold)
        return data


    @staticmethod
    def parse(folder: Path, DIS_threshold=None) -> DisoPredData :
        """
         Parses the prediction output files and add the data inside the
         above attribute data structures.

         Parameters
         ----------
         folder : path to the folder where prediction data is generated

         DIS_threshold : float with values between 0. and 1. (default=0.50)
             Threshold used for disorder class definition.

         Returns:
         -------
         DisoPredData: with parsed data
         """

        data = DisoPredData()

        data.DIS_threshold = DIS_threshold if (DIS_threshold is not None and 0.0 < DIS_threshold < 1.0) \
            else 0.50

        try:
            files = list(folder.rglob('*.diso'))
            if len(files) > 1:
                print("Multiple options: ", list)
                raise
            elif len(files) == 0:
                print("In the folder there is no file with suffix : diso")
                raise
            else:
                diso = files[0]

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        data = data.parsefiles( diso, data.DIS_threshold )

        return data

    @staticmethod
    def __readdiso( file: Path, DIS_threshold : float) -> Tuple[List[str], List[str], List[float]] :
        """
        Parses "*.diso" output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        fileName : Path
        DIS_threshold : float
            Threshold for disorder class definition

        Raises
        ------
        OSError
        Other errors
        """

        seq = []
        DIS_classes = []
        DIS_proba = []

        try:
            f = open(file, 'r')
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

