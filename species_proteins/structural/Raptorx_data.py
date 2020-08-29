from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys


@dataclass
class Raptorx_data:
    """Class that parses RaptorX-property prediction output data.

    Attributes
    ----------

    DIS_threshold: float
        probability threshold for DisPRO disorder prediction class
        definition, default=0.50

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
    parse ( folder : Path, DIS_threshold: float ) -> Raptorx_data
        Parses the RaptorX prediction output files and add the data inside the above attribute data structures. Passed
        as arguments are the folder name (according to raptorX provided output folder) and optionally a threshold for
        disorder.

    parsefiles(ss3: Path, ss8: Path, acc: Path, diso: Path, tgt2: Path, DIS_threshold=None) -> Raptorx_data:
        Parses the RaptorX prediction output files and add the data inside the above attribute data structures. Passed
        as arguments are the files paths and optionally a threshold for disorder.
    """

    sequence: list
    SS3_classes: list
    SS3_proba: list
    SS3_conf: list
    SS8_classes: list
    SS8_proba: list
    ACC3_classes: list
    ACC3_proba: list
    ACC3_conf: list
    DIS_classes: list
    DIS_proba: list
    DIS_threshold: float = 0.5

    @staticmethod
    def parse_files(ss3: Path, ss8: Path, acc: Path, diso: Path, tgt2: Path, DIS_threshold=None) -> Raptorx_data:
        """
        Parses the RaptorX prediction output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        ss3 : path to *.ss3 file
        ss8 : path to *.ss8 file
        acc : path to *.acc file
        diso : path to *.diso file
        tgt2 : path to *.tgt2 file
        DIS_threshold : float with values between 0. and 1. (default=0.50)
            Threshold used for disorder class definition.

        Returns:
        -------
        Raptorx_data: with parsed data
        """

        DIS_threshold = DIS_threshold if (DIS_threshold is not None and 0.0 < DIS_threshold < 1.0) else 0.50

        sequence, SS3_classes, SS3_proba = Raptorx_data.__readss3(ss3)
        SS8_classes, SS8_proba = Raptorx_data.__readss8(ss8)
        ACC3_classes, ACC3_proba = Raptorx_data.__readacc(acc)
        DIS_classes, DIS_proba = Raptorx_data.__readdiso(diso, DIS_threshold)

        SS3_conf, ACC3_conf = Raptorx_data.__readconf(tgt2)

        return Raptorx_data(sequence=sequence, SS3_classes=SS3_classes, SS3_proba=SS3_proba, SS8_classes=SS8_classes, \
                            SS8_proba=SS8_proba, ACC3_classes=ACC3_classes, ACC3_proba=ACC3_proba, \
                            DIS_classes=DIS_classes, DIS_proba=DIS_proba, SS3_conf=SS3_conf, ACC3_conf=ACC3_conf, \
                            DIS_threshold=DIS_threshold )

    @staticmethod
    def parse(folder: Path, DIS_threshold=None) -> Raptorx_data :
        """
         Parses the RaptorX prediction output files and add the data inside the
         above attribute data structures.

         Parameters
         ----------
         folder : path to the folder where prediction data is generated

         DIS_threshold : float with values between 0. and 1. (default=0.50)
             Threshold used for disorder class definition.

         Returns:
         -------
         Raptorx_data: with parsed data
         """

        DIS_threshold = DIS_threshold if (DIS_threshold is not None and 0.0 < DIS_threshold < 1.0) else 0.50

        paths = { 'ss3' : Path(),
                    'ss8' : Path(),
                    'diso' : Path(),
                    'acc' : Path(),
                    'tgt2' : Path(),
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

        return Raptorx_data.parse_files(paths['ss3'], paths['ss8'], paths['acc'], paths['diso'], \
                                        paths['tgt2'], DIS_threshold)


    @staticmethod
    def __readdiso(file: Path, DIS_threshold: float) -> Tuple[List[str], List[float]]:
        """
        Parses "*.diso" output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        file: Path
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
            f = open(file, 'r')
            lines = f.readlines()
            for line in lines:
                l = line.split()
                if l[0][0] != '#':
                    current = float(l[3])
                    DIS_proba.append(current)
                    if current >= DIS_threshold:
                        DIS_classes.append('D')
                    else:
                        DIS_classes.append('-')
        except OSError:
            print("File error:", sys.exc_info()[0])
            raise
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return DIS_classes, DIS_proba


    @staticmethod
    def __readss3(file: Path) -> Tuple[List[str], List[str], List[Dict[str, float]]] :
        """
        Parses "*.ss3" output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        fileName : path
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
            f = open(file, 'r')
            lines = f.readlines()
            for line in lines:
                l = line.split()
                if l[0][0] != '#':
                    Hproba = float(l[3])
                    Eproba = float(l[4])
                    Cproba = float(l[5])
                    ss = l[2]

                    seq.append(l[1])
                    SS3_proba.append({"H": Hproba,
                                      "E": Eproba,
                                      "C": Cproba})
                    SS3_classes.append(ss)

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return seq, SS3_classes, SS3_proba

    @staticmethod
    def __readss8(file: Path) -> Tuple[List[str], List[Dict[str, float]]] :
        """
        Parses "*.ss8" output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        fileName : path
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
            f = open(file, 'r')
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

                    SS8_proba.append({"H": Hproba,
                                      "G": Gproba,
                                      "I": Iproba,
                                      "E": Eproba,
                                      "B": Bproba,
                                      "T": Tproba,
                                      "S": Sproba,
                                      "C": Cproba})

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

    @staticmethod
    def __readacc(file: Path) -> Tuple[List[str], List[Dict[str, float]]] :
        """
        Parses "*.acc" output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        file : Path

        Raises
        ------
        OSError
        Other errors
        """

        # for cases when the method is called twice
        ACC3_classes = []
        ACC3_proba = []

        try:
            f = open(file, 'r')
            lines = f.readlines()
            for line in lines:
                l = line.split()
                if l[0][0] != '#':
                    Bproba = float(l[3])
                    Mproba = float(l[4])
                    Eproba = float(l[5])

                    acc = l[2]

                    ACC3_proba.append({"B": Bproba,
                                       "M": Mproba,
                                       "E": Eproba})
                    ACC3_classes.append(acc)

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return ACC3_classes, ACC3_proba

    @staticmethod
    def __readconf(file: Path) -> Tuple[List[int], List[int]]:
        """
        Parses "*.tgt2" output files and add the data inside the
        above attribute data structures.

        Parameters
        ----------
        file: Path

        Raises
        ------
        OSError
        Other errors
        """

        # for cases when the method is called twice
        ACC3_conf = []
        SS3_conf = []

        try:
            f = open(file, 'r')
            lines = f.readlines()
            for line in lines:
                l = line.split()
                if len(l) > 2 and l[0] == 'SSEconf':
                    SS3conf = l[2]
                if len(l) > 2 and l[0] == 'ACCconf':
                    ACCconf = l[2]

            for it in range(len(SS3conf)):
                SS3_conf.append(int(SS3conf[it]))
                ACC3_conf.append(int(ACCconf[it]))

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return SS3_conf, ACC3_conf


