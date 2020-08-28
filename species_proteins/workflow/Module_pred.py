from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from species_proteins.util.util import map_aln
import sys


@dataclass
class Module_pred :
    """Base class that organises different module predictions output

    Attributes
    ----------

    Public Methods
    --------------
    print_1prot( self )
        Prints all predictions in a vertical layout
        For single protein profile layout

    print_Nprot( self )
        Prints all predictions in a vertical layout
        For multi protein profile layout

    """

    paths: dict
    predictions : dict
    module = ''
    availPredictors = []
    header = []

    def print_1prot(self: Module_pred, outputfile: Path, protname: str = None, addseq: bool = True,
                    signif: bool = False):

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
            print("#Module:", self.module, sep='\t', file=output)
            print("#Protname: ", protname, sep='\t', file=output)
            print("\n", file=output)

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
            print("#Module", self.module, sep='\t', file=output)
            print("#Alnfile: ", alnfile, sep='\t', file=output)
            print("\n", file=output)

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


    def parse_all(paths: dict) -> Module_pred:
        """Virtual"""
        raise NotImplementedError()


    def get_layout_1prot(self: Module_pred, protname: str, signif: bool = False) -> dict:

        data = self.predictions[protname]
        seq = data['seq'];
        protsize = len(seq)

        layout = {}
        for entry in self.header:
            pred = entry[0]
            type = entry[1]
            enzyme = entry[2]
            key = pred + "_" + type + "_" + enzyme
            layout[key] = ['X' if pred not in data else '-' for resid in range(protsize)]

        for pred in self.availPredictors:
            for resid in data[pred]:
                for entry in data[pred][resid]:
                    start = entry['start'] - 1
                    end = entry['end'] - 1
                    score = entry['score']
                    type = entry['type']

                    if pred == 'gpspail':
                        enzyme = entry['enzyme']
                    elif self.module == "Phosphorylation":
                        type = 'STY-phos'
                        enzyme = 'generic'
                    else: enzyme='N/A'

                    key = pred + "_" + type + "_" + enzyme

                    for id in range(start, end + 1):
                        if signif:
                            if entry['is_signif']: layout[key][id] = score
                        elif pred == 'netphos' and entry['enzyme'] == 'unsp':
                            # we print only generic predictions as there are too many kinases
                            layout[key][id] = score
                        else:
                            layout[key][id] = score
        return layout



