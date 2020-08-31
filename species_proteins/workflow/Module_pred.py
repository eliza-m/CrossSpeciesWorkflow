from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from species_proteins.util.util import map_aln
import sys


@dataclass
class Module_pred :
    """
    Base class that organises different module predictions output

    Attributes
    ----------
    paths :  dict
        Dictionary with raw prediction data.

    predictions : dict
        Dictionary with all parsed predictions.

    module : string
        Module name. Specific to each child class

    availPredictors : list
        List of available predictors. Specific to each child class

    header : list
        Printing header specific to each child class.


    Public Methods
    --------------

    parse_all(paths: dict) -> Module_pred:
        Virtual method implemented in each child class.


    print_1prot(self: Module_pred, outputfile: Path, protname: str = None, addseq: bool = True,
                    signif: bool = False)
        Prints all predictions in a vertical layout
        For single protein profile layout.

        Arguments:
            - self          : Module_pred [required]

            - outputfile    : Path. Filename for results summary output [required]

            - protname      : String. Protname key to print if in the parsed data are multiple protname keys.
                            If not provided and a single protname key exists it will print it,
                            but if multiple protname keys are found an error will be raised to provide
                            as argument the specific protname to print. [Optional. Default: None]

            - addseq        : Boolean. If true prints resid and aminoacid columns. [Optional. Default: True]

            - signif        : Boolean. If true prints only significant predicted sites. Significance thresholds are
                            predictor specific. [Optional. Default: False]


    print_Nprot(self: Module_pred, alnfile: Path, outputfile: Path, addseq: bool = True,
                    signif: bool = False)
        Prints all predictions in a vertical layout
        For multi protein profile layout, showing sequences aligned.

        Arguments:
            - self          : Module_pred [required]

            - alnfile       : Path. Alignment file to use in multi FASTA format. [required]

            - outputfile    : Path. Filename for results summary output [required]

            - protname      : String. Protname key to print if in the parsed data are multiple protname keys.
                            If not provided and a single protname key exists it will print it,
                            but if multiple protname keys are found an error will be raised to provide
                            as argument the specific protname to print. [Optional. Default: None]

            - addseq        : Boolean. If true prints resid and aminoacid columns. [Optional. Default: True]

            - signif        : Boolean. If true prints only significant predicted sites. Significance thresholds are
                            predictor specific. [Optional. Default: False]


    get_layout_1prot(self: Module_pred, protname: str, signif: bool = False) -> dict
        Get a vertical layout of the predicted data for each protein sequences, as multiple classes that
        inherits module_pred keep only a dictionary with the predicted sites, and do not track resids and resnames.

        Arguments:
            - self          : Module_pred [required]

            - protname      : String. Protname key to to obtain layout of. [required]

            - signif        : Boolean. If true prints only significant predicted sites. Significance thresholds are
                            predictor specific. [Optional. Default: False]

    """

    paths: dict
    predictions : dict
    module = ''
    availPredictors = []
    header = []


    def parse_all(paths: dict) -> Module_pred:
        """Virtual method implemented in each child class."""
        raise NotImplementedError()



    def print_1prot(self: Module_pred, outputfile: Path, protname: str = None, addseq: bool = True,
                    signif: bool = False):
        """
        Prints all predictions in a vertical layout. For single protein profile layout.

        Parameters
        ----------
        outputfile: Path
            Filename for results summary output [required]

        protname : String
            Protname key to print if in the parsed data are multiple protname keys.
            If not provided and a single protname key exists it will print it,
            but if multiple protname keys are found an error will be raised to provide
            as argument the specific protname to print. [Optional. Default: None]

        addseq: Boolean
            If true prints resid and aminoacid columns. [Optional. Default: True]

        signif: Boolean
            If true prints only significant predicted sites. Significance thresholds are
            predictor specific. [Optional. Default: False]

        Returns
        -------
        """

        try:
            output = open(outputfile, 'w')

            if protname is None:
                keys = list(self.predictions.keys())
                if len(keys) > 1:
                    print(
                        "Please provide protein name, as predictions from multiple proteins were detected within the specified folder")
                    raise
                else:
                    protname = keys[0]

            layout= self.get_layout_1prot(protname, signif)

            # Print header
            # print("#Module:", self.module, sep='\t', file=output)
            # if self.module == "Structural" :
            #     print("#DIS_threshold:", self.DIS_threshold, sep='\t', file=output)
            #   # print("#ACC_threshold (only for scratch1d):", self.DIS_threshold, sep='\t', file=output)
            # print("#Protname: ", protname, sep='\t', file=output)
            # print("\n", file=output)

            if addseq:
                print('{:>6}{:>5}'.format('resid', 'aa'), sep='\t', end='\t', file=output)

            for l in range(3):
                if l>0 and addseq:
                    print('{:>6}{:>5}'.format('_', '_'), sep='\t', end='\t', file=output)
                for entry in self.header:
                    print('{:>12}'.format(entry[l]), end='\t', file=output)
                print(file=output)

            seq = self.predictions[protname]['seq']
            for id in range( len(seq) ) :
                if addseq:
                    print('{:>6}{:>5}'.format(id + 1, seq[id]), sep='\t', end='\t', file=output)

                for entry in self.header:
                    key = entry[0] + '_' + entry[1] + '_' + entry[2]
                    print('{:>12}'.format(layout[key][id]), end='\t', file=output)
                print(file=output)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise




    def print_Nprot(self: Module_pred, alnfile: Path, outputfile: Path, addseq: bool = True,
                    signif: bool = False):
        """
        Prints all predictions in a vertical layout. For multi protein profile layout, showing sequences aligned.

        Parameters
        ----------
        alnfile: Path
            Alignment file to use in multi FASTA format. [required]

        outputfile: Path
            Filename for results summary output [required]

        protname : String
            Protname key to print if in the parsed data are multiple protname keys.
            If not provided and a single protname key exists it will print it,
            but if multiple protname keys are found an error will be raised to provide
            as argument the specific protname to print. [Optional. Default: None]

        addseq: Boolean
            If true prints resid and aminoacid columns. [Optional. Default: True]

        signif: Boolean
            If true prints only significant predicted sites. Significance thresholds are
            predictor specific. [Optional. Default: False]

        Returns
        -------
        """

        try:
            output = open(outputfile, 'w')

            alnmapping = map_aln(alnfile)

            size = []
            for prot in alnmapping:
                keys = list(self.predictions.keys())
                size.append( len(alnmapping[prot]['seq']) )
                if prot not in keys:
                    print(prot +
                          " predictions not detected within the specified folder")
                    raise

                alnmapping[prot]['layout'] = self.get_layout_1prot(prot, signif)


            # Print header
            # print("#Module", self.module, sep='\t', file=output)
            # print("#Alnfile: ", alnfile, sep='\t', file=output)
            # if self.module == "Structural" :
            #     print("#DIS_threshold:", self.DIS_threshold, sep='\t', file=output)
            #   # print("#ACC_threshold (only for scratch1d):", self.DIS_threshold, sep='\t', file=output)
            # print("\n", file=output)

            if addseq:
                print('{:>6}'.format('alnid'), sep='\t', end='\t', file=output)
                for prot in alnmapping:
                    print('{:>7}'.format(prot), sep='\t', end='\t', file=output)
                print('{:>3}'.format('Dif'), sep='\t', end='\t', file=output)

            for l in range(3):
                if l > 0 and addseq:
                    print('{:>6}'.format('N/A'), sep='\t', end='\t', file=output)
                    for prot in alnmapping:
                        print('{:>7}'.format('N/A'), sep='\t', end='\t', file=output)
                    print('{:>3}'.format('N/A'), sep='\t', end='\t', file=output)

                for entry in self.header:
                    for prot in alnmapping:
                        print('{:>12}'.format(entry[l]), end='\t', file=output)
                print(file=output)


            if addseq:
                print('{:>6}'.format('N/A'), sep='\t', end='\t', file=output)
                for prot in alnmapping:
                    print('{:>7}'.format('N/A'), sep='\t', end='\t', file=output)
                print('{:>3}'.format('N/A'), sep='\t', end='\t', file=output)

            for entry in self.header:
                for prot in alnmapping:
                    print('{:>12}'.format(prot), end='\t', file=output)
            print(file=output)


            # Print data
            for alnid in range(size[0]):
                if addseq:
                    print('{:>6}'.format(alnid + 1), sep='\t', end='\t', file=output)
                    s = ''
                    for prot in alnmapping:
                        aa = alnmapping[prot]['seq'][alnid]
                        s += aa
                        print('{:>7}'.format(aa), sep='\t', end='\t', file=output)

                    dif = ' ' if len(set(s)) == 1 else '*'
                    print('{:>3}'.format(dif), sep='\t', end='\t', file=output)


                for entry in self.header:
                    key = entry[0] + '_' + entry[1] + '_' + entry[2]
                    for prot in alnmapping:
                        resid = alnmapping[prot]['mapid'][alnid] - 1
                        print('{:>12}'.format(alnmapping[prot]['layout'][key][resid]), end='\t', file=output)
                print(file=output)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise







    def get_layout_1prot(self: Module_pred, protname: str, signif: bool = False) -> dict:
        """
        Get a vertical layout of the predicted data for each protein sequences, as multiple classes that
        inherits module_pred keep only a dictionary with the predicted sites, and do not track resids and resnames.

        Parameters
        ----------
        protname: string
            Protname key to to obtain layout of. [required]

        signif: Boolean
            If true prints only significant predicted sites. Significance thresholds are
            predictor specific. [Optional. Default: False]

        Returns
        -------
        layout: dict
            Formated layout for a specific protein sequence and predictor.
        """

        data = self.predictions[protname]
        seq = data['seq'];
        protsize = len(seq)

        layout = {}
        for entry in self.header:
            pred = entry[0]
            type = entry[1]
            details = entry[2]
            key = pred + "_" + type + "_" + details
            layout[key] = ['X' if pred not in data else '-' for resid in range(protsize)]

        for pred in self.availPredictors:
            for resid in data[pred]:
                for entry in data[pred][resid]:
                    start = entry['start'] - 1
                    end = entry['end'] - 1
                    score = entry['score']
                    type = entry['type']

                    if pred == 'gpspail':
                        details = entry['enzyme']
                    elif self.module == "Phosphorylation":
                        type = 'STY-phos'
                        details = 'generic'
                    elif self.module == "Localisation":
                        type = 'TM'
                        details = '3-class'
                    else: details='N/A'

                    key = pred + "_" + type + "_" + details

                    for id in range(start, end + 1):
                        if signif:
                            if entry['is_signif']: layout[key][id] = score
                        elif pred == 'netphos' and entry['enzyme'] == 'unsp':
                            # we print only generic predictions as there are too many kinases
                            layout[key][id] = score
                        elif pred in ['tmpred', 'tmhmm'] :
                            layout[key][id] = entry['loc']
                        else:
                            layout[key][id] = score
        return layout



