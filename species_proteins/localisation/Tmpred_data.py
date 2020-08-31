from __future__ import annotations
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from time import sleep
from bioservices.apps import FASTA

import requests


@dataclass
class Tmpred_data:
    """Class that parses Tmpred prediction output data.

    Attributes
    ----------
    predicted_sites : Dictionary
        predicted_sites [ protein name ][ start resid ] : array of entry dict
        entry dict has the following keys:

        # Common to all PTM predictors
            seq : string (stretch of the predicted sequence)
            start : starting residue id
            end : ending residue id
            is_signif : bool (is the method's specific scoring indicating a
                            potentially significant result)
            score : float (interpretation differs between methods)
            type : string
            predictor : string (for cases where multiple predictors are available)

        # Additional fields:
            loc: Predicted localisation

    Public Methods
    --------------
    parse( outputfile : path ) -> Tmpred_data
        Parses the prediction output file and add the data inside the
        above attribute data structure.

    submit_online (fastafile : Path, outputfile: Path)
        Submits online job. Provided as arguments are the input fasta file and the
        prediction output file paths

    """

    predicted_sites: dict

    @staticmethod
    def parse(outputfile: Path) -> Tmpred_data:
        """Parses predictor's output"""

        predicted_sites = {}
        name = outputfile.name
        protname = name.split('.')[0]
        predicted_sites[protname] = {}

        try:
            f = open(outputfile, 'r')
            lines = f.readlines()
            if "Failed: Online job submission failed" in lines[0]:
                return Tmpred_data(predicted_sites)

            is_section = False
            found = False
            lastaa = 1
            for line in lines:
                if 'length:' in line:
                    size = int( line.split()[-1] )
                elif "STRONGLY prefered model" in line:
                    is_section = True; found = True
                elif "alternative model" in line:
                    is_section = False
                elif is_section:
                    l = line.split()
                    if len(l) == 6 and l[0][0] not in '<#':
                        start = int(l[1])
                        end = int(l[2])
                        seg = l[5]
                        score = int(l[4])

                        resid = lastaa
                        loc = 'IN' if seg == "i-o" else "OUT"
                        nextloc = 'OUT' if seg=="i-o" else 'IN'

                        if resid not in predicted_sites[protname]:
                            predicted_sites[protname][resid] = []

                        predicted_sites[protname][resid].append({
                            "seq": '',
                            "start": resid,
                            "end": start-1,
                            "is_signif": "YES",
                            "score": score,
                            "loc": loc,
                            "type": "TMhelix",
                            "predictor": "tmpred_online"
                        })

                        resid = start
                        loc = 'TMhelix'
                        lastaa = end + 1

                        if resid not in predicted_sites[protname]:
                            predicted_sites[protname][resid] = []

                        predicted_sites[protname][resid].append({
                            "seq": '',
                            "start": resid,
                            "end": end,
                            "is_signif": "YES",
                            "score": score,
                            "loc": loc,
                            "type": "TM",
                            "predictor": "tmpred_online"
                        })

            # Add last segment if present
            if found: 
                resid = lastaa
                if resid not in predicted_sites[protname]:
                    predicted_sites[protname][resid] = []

                predicted_sites[protname][resid].append({
                    "seq": '',
                    "start": resid,
                    "end": size,
                    "is_signif": "YES",
                    "score": score,
                    "loc": nextloc,
                    "type": "TM",
                    "predictor": "tmpred_online"
                })

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        print(predicted_sites)
        return Tmpred_data(predicted_sites)


    @staticmethod
    def submit_online(fastafile: Path, outputfile: Path):
        """Submits online job. Provided as arguments are the input fasta file and the
                        prediction output filename"""

        try:
            # launch job
            url = 'https://embnet.vital-it.ch/cgi-bin/TMPRED_form_parser'
            f = FASTA()
            f.read_fasta(fastafile)
            seq = f.sequence

            data = {
                    'outmode':'html',
                    'min': '17',
                    'max': '33',
                    'comm': '',
                    'format' : 'plain_text',
                    'seq': seq
                    }
            s = requests.session()
            r1 = s.post(url, data=data)
            r1.raise_for_status()

            # write results
            file = open(outputfile, "w")
            file.write(r1.text)

        except Exception as e:
            print("Failed: Online job submission failed !!!!")
            if hasattr(e, 'message'): print(e.message)
            else: print(e)
            with open(outputfile, 'w', encoding='utf-8') as f:
                print("#Failed: Online job submission failed !!!! Error: ", e, file=f)
            pass