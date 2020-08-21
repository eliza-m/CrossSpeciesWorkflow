from __future__ import annotations
from tinyfasta import FastaParser
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import sys
from .NetNglycData import NetNglycData
from .NetOglycData import NetOglycData
from .NetCglycData import NetCglycData
from .GlycomineData import GlycomineData
from .IsoglypData import IsoglypData
from .NGlyDEData import NGlyDEData


@dataclass
class GlycosylationPred :
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
    def parseall(paths: dict) -> GlycosylationPred:
        """
        Parses all the prediction output files and add the data inside the
        above attribute data structures.
        """

        predictions = {}

        for prot in paths:
            for predictor in paths[prot]:

                if predictor.lower() == "netnglyc":
                    data = NetNglycData.parse(paths[prot][predictor])
                elif predictor.lower() == "netoglyc":
                    data = NetOglycData.parse(paths[prot][predictor])
                elif predictor.lower() == "netcglyc":
                    data = NetCglycData.parse(paths[prot][predictor])
                elif predictor.lower() == "isoglyp":
                    data = IsoglypData.parse(paths[prot][predictor])
                elif predictor.lower() == "glycomine":
                    data = GlycomineData.parse(paths[prot][predictor])
                elif predictor.lower() == "nglyde":
                    data = NglyDEData.parse(paths[prot][predictor])

                # adding the fasta file data
                elif predictor.lower() == "fasta":
                    fasta = FastaParser(paths[prot][predictor])
                    if fasta.description.contains(prot):
                        data = fasta.sequence
                    else:
                        print("Protein name ", prot, "is not contained in the provided fasta file")
                        raise
                    predictor="seq"

                else:
                    print("Unknown predictor key: ", predictor)
                    raise

                if prot not in data.predictions:
                    predictions[prot] = {}

                predictions[prot][predictor] = data

        return GlycosylationPred(predictions)



    def print1prot( self : GlycosylationPred, protname: str, addseq: bool ):

        try:

            data = self.predictions[ protname ]

            predictors = ['']

            # Print header
            print("#Module: Glycosylation", sep='\t')
            print("#Protname: ", protname, sep='\t')
            print("\n")

            if addseq :
                print( "#resid", "aa", sep='\t', end='\t')

            print("_", "NetNglyc_N", "NglyDE_N", "Glycomine_N", \
                  "_", "NetOglyc_O", "Isoglyp_O", "Glycomine_O"\
                  "_", "NetCglyc_C", "Glycomine_N", sep='\t')

            seq = self.sequence
            protsize = len(seq)


            for id in range(protsize):

                if addseq:
                    print(id + 1, seq[id], sep='\t', end='\t')

                values = []
                if id in data["netnglyc"]:
                    values.append( data["netnglyc"][id]["score"] if data["netnglyc"][id]["isSignif"] else '-')

                if id in data["nglyde"]:
                    values.append( data["nglyde"][id]["score"] if data["nglyde"][id]["isSignif"] else '-')

                if id in data["glycomine"]:
                    values.append( data["glycomine"]['N'][id]["score"] if data["glycomine"]['N'][id]["isSignif"] else '-')

                if id in data["netoglyc"]:
                    values.append( data["netoglyc"][id]["score"] if data["netoglyc"][id]["isSignif"] else '-')

                if id in data["isoglyp"]:
                    values.append( data["isoglyp"][id]["score"] if data["isoglyp"][id]["isSignif"] else '-')

                if id in data["glycomine"]:
                    values.append( data["glycomine"]['O'][id]["score"] if data["glycomine"]['O'][id]["isSignif"] else '-')

                if id in data["netcglyc"]:
                    values.append( data["netcglyc"][id]["score"] if data["netcglyc"][id]["isSignif"] else '-')

                if id in data["glycomine"]:
                    values.append( data["glycomine"]['C'][id]["score"] if data["glycomine"]['C'][id]["isSignif"] else '-')

                for val in values:
                    print(val, sep='\t')
                print()


        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
