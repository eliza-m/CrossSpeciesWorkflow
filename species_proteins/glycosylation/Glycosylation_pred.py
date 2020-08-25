from __future__ import annotations
from bioservices.apps import FASTA
from dataclasses import dataclass, field
from pathlib import Path
import sys
from .Netnglyc_data import Netnglyc_data
from .Netoglyc_data import Netoglyc_data
from .Netcglyc_data import Netcglyc_data
from .Glycomine_data import Glycomine_data
from .Isoglyp_data import Isoglyp_data
from .Nglyde_data import Nglyde_data

# in the printing order
avail_predictors = ["netnglyc", "nglyde", "glycomineN", "netoglyc", "isoglyp", "glycomineO", "netcglyc", "glycomineC"]


@dataclass
class Glycosylation_pred :
    """Class that organises Structural Predictions output for single protein

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
    def parse_all(paths: dict) -> Glycosylation_pred:
        """
        Parses all the prediction output files and add the data inside the
        above attribute data structures.
        """

        predictions = {}

        for prot in paths:
            for predictor in paths[prot]:

                if predictor == "netnglyc":
                    data = Netnglyc_data.parse(paths[prot][predictor])
                elif predictor == "netoglyc":
                    data = Netoglyc_data.parse(paths[prot][predictor])
                elif predictor == "netcglyc":
                    data = Netcglyc_data.parse(paths[prot][predictor])
                elif predictor == "isoglyp":
                    data = Isoglyp_data.parse(paths[prot][predictor])
                elif predictor == "nglyde":
                    data = Nglyde_data.parse(paths[prot][predictor])
                elif predictor == "glycomineN":
                    data = Glycomine_data.parse(paths[prot][predictor])
                elif predictor == "glycomineO":
                    data = Glycomine_data.parse(paths[prot][predictor])
                elif predictor == "glycomineC":
                    data = Glycomine_data.parse(paths[prot][predictor])

                # adding the fasta file data
                elif predictor in ["fasta", "fsa"]:
                    # this needs to be further moved as a function that properly checks for multiprotein file 
                    # or for alignments 

                    f = FASTA()
                    f.read_fasta(paths[prot][predictor])
                    if prot in f.header :
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


        return Glycosylation_pred(paths, predictions)



    def print_1prot(self : Glycosylation_pred, outputfile: Path, protname: str = None, addseq: bool = True, signif: bool = False):

        try:

            output = open(outputfile, 'w')

            if protname is None:
                keys = list( self.predictions.keys() )
                if len(keys)>1:
                    print("Please provide protein name, as predictions from multiple proteins were detected within the specified folder")
                    raise
                else:
                    protname = keys[0]

            data = self.predictions[ protname ]

            # Print header
            print("#Module: Glycosylation", sep='\t', file=output)
            print("#Protname: ", protname, sep='\t', file=output)
            print("\n", file=output)

            if addseq :
                print( '{:>6}{:>5}'.format("#resid", "aa"), sep='\t', end='\t', file=output)

            header = [ "NetNglyc_N", "NglyDE_N", "Glycomine_N", \
                  "NetOglyc_O", "Isoglyp_O", "Glycomine_O", \
                  "NetCglyc_C", "Glycomine_C" ]

            for item in header:
                print( '{:>12}'.format( item ), end='\t', file=output )
            print(file=output)

            seq = data['seq'];
            protsize = len(seq)

            # contains predictions in the desired format for printing
            values = {}
            for p in avail_predictors:

                if p not in data :
                    # if predictor's data is not available (i.e prediction was not performed)
                    values[p] = ['X' for resid in range(protsize) ]

                else:
                    # we do not use 0 as, if signif is selected true, predictions with lower scores than significance
                    # threshold would have score 0 which is misleading.
                    values[p] = ['-' for resid in range(protsize) ]; 

                    # adding prediction results
                    for resid in data[p]:
                        for entry in data[p][resid]:
                            start = entry['start'] - 1
                            end = entry['end'] - 1
                            score = entry['score']
                         
                            for resid in range(start, end + 1):
                                # if we have overlaping predictions we choose the one with higher scores
                                if values[p][resid] != '-' and score > values[p][resid]:
                                    continue
                                else:
                                    if signif:
                                        if entry['is_signif'] : values[p][resid] = score 
                                    else:
                                        values[p][resid] = score

            for id in range(protsize):

                if addseq:
                    print('{:>6}{:>5}'.format(id+1, seq[id]), sep='\t', end='\t', file=output)

                for p in avail_predictors:
                    print( '{:>12}'.format(values[p][id]), end='\t', file=output )
                print(file=output)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

