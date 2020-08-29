from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import *


@dataclass
class Psipred_data:
    """Class that parses PsiPred prediction output data.

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
    parse ( folder : Path ) -> Psipred_data
        Parses the prediction output files and add the data inside the above attribute data structures. Passed
        as arguments are the folder name (the PsiPred output folder).

    parse_files(ss2: Path, horiz Path ) -> Psipred_data:
        Parses the PsiPred prediction output files and add the data inside the above attribute data structures. Passed
        as arguments are the files paths.
    """


    sequence: list
    SS3_classes: list
    SS3_proba: list
    SS3_conf: list


    @staticmethod
    def parse_files(ss2: Path, horiz: Path ) -> Psipred_data:
        """
        Parses the prediction output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        ss2 : path to *.ss2 file
        horiz : path to *.horiz file

        Returns:
        -------
        Psipred_data: with parsed data
        """

        sequence, SS3_classes, SS3_proba = Psipred_data.__readss2(ss2)
        SS3_conf = Psipred_data.__readconf(horiz)

        return Psipred_data(sequence=sequence, SS3_classes=SS3_classes, SS3_proba=SS3_proba, SS3_conf=SS3_conf )


    @staticmethod
    def parse(folder: Path) -> Psipred_data :
        """
         Parses the PsiPred prediction output files and add the data inside the
         above attribute data structures.

         Parameters
         ----------
         folder : path to the folder where prediction data is generated

         Returns:
         -------
         Psipred_data: with parsed data
         """

        paths = { 'ss2' : Path(), 'horiz' : Path() }

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
        return Psipred_data.parse_files( paths['ss2'], paths['horiz'] )



    @staticmethod
    def __readss2( file : Path ) -> Tuple[List[str], List[str], List[Dict[str, float]]] :
        """
        Parses "*.ss2" output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        file : Path

        Raises
        ------
        OSError
        Other errors

        Returns
        ------
        (seq, SS3_classes, SS3_proba) : Tuple( list, list, list )
            intermediary lists containing parsed data
        """

        seq = []
        SS3_classes = []
        SS3_proba = []
        try:
            f = open(file, 'r')
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


    @staticmethod
    def __readconf( file : Path ) -> List[int] :
        """
        Parses "*.horiz" output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        file : Path

        Raises
        ------
        OSError
        Other errors

        Returns
        ------
        SS3_conf : list
            Intermediary lists containing parsed data
        """

        SS3_conf = []
        try:
            f = open(file, 'r')
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


