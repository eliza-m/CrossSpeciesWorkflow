from __future__ import annotations
from bioservices.apps import FASTA
from dataclasses import dataclass
from pathlib import Path
import sys
from .Gpspail_data import Gpspail_data
from .Netacet_data import Netacet_data

# in the printing order
AvailPredictors = ["netacet", "gpspail"]


@dataclass
class Acetylation_pred:
    """Class that organises Acetylation module output for single protein

    Attributes
    ----------

    Public Methods
    --------------
    parseall()
        Parses all the prediction output files and add the data inside the
        above attribute data structures.

    print1prot( self )
        Prints all predictions in a vertical layout
        For single protein profile layout

    printNprot( self )
        Prints all predictions in a vertical layout
        For multi protein profile layout

    """

    paths: dict
    predictions: dict

    @staticmethod
    def parse_all(paths: dict) -> AcetylationPred:
        """
        Parses all the prediction output files and add the data inside the
        above attribute data structures.
        """

        predictions = {}

        for prot in paths:
            for predictor in paths[prot]:

                if predictor == "netacet":
                    data = Netacet_data.parse(paths[prot][predictor])
                elif predictor == "gpspail":
                    data = Gpspail_data.parse(paths[prot][predictor])

                # adding the fasta file data
                elif predictor in ["fasta", "fsa"]:
                    # this needs to be further moved as a function that properly checks for multiprotein file 
                    # or for alignments 

                    f = FASTA()
                    f.read_fasta(paths[prot][predictor])
                    if prot in f.header:
                        seq = f.sequence
                    else:
                        print("Protein name ", prot, "is not contained in the provided fasta file")
                        raise

                else:
                    print("Unknown predictor key: ", predictor)
                    raise

                if prot not in predictions:
                    predictions[prot] = {}

                predictions[prot][predictor] = data.predicted_sites[prot]
            predictions[prot]['seq'] = seq

        return Acetylation_pred(paths, predictions)



    def print_1prot(self: AcetylationPred, outputfile: Path, protname: str = None, addseq: bool = True,
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

            data = self.predictions[protname]

            # Print header
            print("#Module: Acetylation", sep='\t', file=output)
            print("#Protname: ", protname, sep='\t', file=output)
            print("\n", file=output)


            header = [
                ["NetAcet", "Nter-acet" , "" ],
                ["GpsPail", "K-acet", "CREBBP"],
                ["GpsPail", "K-acet", "EP300"],
                ["GpsPail", "K-acet", "HAT1"],
                ["GpsPail", "K-acet", "KAT2A"],
                ["GpsPail", "K-acet" , "KAT2B" ],
                ["GpsPail", "K-acet", "KAT5"],
                ["GpsPail", "K-acet", "KAT8"],
            ]

            for line in range(len(header[0])):
                print('#', end='\t', file=output)
                if addseq:
                    if line==1:
                        print('{:>6}{:>5}'.format("resid", "aa"), sep='\t', end='\t', file=output)
                    else: print('{:>6}{:>5}'.format("", ""), sep='\t', end='\t', file=output)
                for entry in header:
                    print( '{:>12}'.format( entry[line] ), end='\t', file=output )
                print(file=output)


            seq = data['seq'];
            protsize = len(seq)

            # contains predictions in the desired format for printing

            values = {}

            values[''] = ['X' if 'netacet' not in data else '-' for resid in range(protsize)]
            for e in Gpspail_data.enzymes:
                values[e] = ['X' if 'gpspail' not in data else '-' for resid in range(protsize)]

            for pred in data:
                for resid in pred:
                    for entry in data[p][resid]:
                        start = entry['start'] - 1
                        end = entry['end'] - 1
                        score = entry['score']

                        key = entry['enzyme'] if pred == 'gpspail' else 'netacet'

                        for resid in range(start, end + 1):
                            if signif:
                                if entry['is_signif']: values[key][resid] = score
                            else:
                                values[key][resid] = score

            for id in range(protsize):

                if addseq:
                    print('{:>6}{:>5}'.format(id + 1, seq[id]), sep='\t', end='\t', file=output)

                for entry in header:
                    key = entry[2]
                    print('{:>12}'.format(values[key][id]), end='\t', file=output)
                print(file=output)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

