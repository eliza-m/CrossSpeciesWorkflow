from __future__ import annotations
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from time import sleep
from bioservices.apps import FASTA

import requests


@dataclass
class Tmhmm_data:
    """Class that parses TMHMM v2.0 prediction output data.

    Parameters
    ----------

    Attributes
    ----------
    predicted_sites : Dictionary
        predicted_sites [ protein name ][ start resid ] : array of entry dict
        entry dict has the following keys:

        # Common to all PTS predictors
            seq : string (stretch of the predicted sequence)
            start : starting residue id
            end : ending residue id
            is_signif : bool (is the method's specific scoring indicating a
                            potentially significant result)
            score : float (interpretation differs between methods)
            type : string (C-glyc)
            predictor : string (for cases where multiple predictors are available)

    Public Methods
    --------------
    parse( outputfile : path ) -> Deeploc_data
        Parses the NetAcet prediction output file and add the data inside the
        above attribute data structure.

    submit_online (fastafile : Path, outputfile: Path)
        Submits online job. Provided as arguments are the input fasta file and the
        prediction output file paths

    """


    predicted_sites : dict


    @staticmethod
    def parse(outputfile: Path) ->Tmhmm_data:

        predicted_sites = {}
        name = outputfile.name
        protname = name.split('.')[0]
        predicted_sites[protname] = {}

        try:
            f = open(outputfile, 'r')
            lines = f.readlines()
            for line in lines:
                l = line.split()
                if len(l) == 5 and l[0][0] not in '<#' :

                    start = int(l[3])
                    end = int(l[4])
                    loc = l[2]
                    score = 'N\A'
                    is_signif = "YES"

                    if loc == 'inside': loc = "IN"
                    elif loc == 'outside': loc = "OUT"
                    else: loc = "TMhelix"

                    resid = start

                    if resid not in predicted_sites[protname]:
                        predicted_sites[protname][resid] = []

                    predicted_sites[protname][resid].append({
                        "seq": '',
                        "start": start,
                        "end": end,
                        "is_signif": is_signif,
                        "score": score,
                        "loc":  loc,
                        "type": "TM",
                        "predictor": "tmhmm:2.0_online"
                    })

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        print(predicted_sites)
        return Tmhmm_data(predicted_sites)


    @staticmethod
    def submit_online (fastafile : Path, outputfile: Path) :

        try:

            #launch job
            url = 'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi'
            f = FASTA()
            f.read_fasta(fastafile)
            seq = f.sequence

            data = {'SEQ': seq, 'configfile':'/var/www/html/services/TMHMM-2.0/webface.cf',
                    'outform': '-noshort'}
            r1 = requests.post(url, data=data)

            #retrieve results
            temp = re.search(r"jobid: .+ status", r1.text)
            jobid = temp.group().split(' ')[1]

            sleep(2)
            r2 = requests.get(url, params={'jobid' : jobid })

            while jobid in r2.text:
                sleep(2)
                r2 = requests.get(url, params={'jobid': jobid })


            r2.raise_for_status()

            file = open(outputfile, "w")
            file.write(r2.text)

        except Exception as e:
            print("Failed: Online job submission failed !!!!")
            if hasattr(e, 'message'): print(e.message)
            else: print(e)
            pass

