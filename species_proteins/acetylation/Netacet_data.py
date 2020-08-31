from __future__ import annotations
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from time import sleep
from bioservices.apps import FASTA

import requests


@dataclass
class Netacet_data:
    """Class that parses NetAcet prediction output data.

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
            enzime: predictions for multple enzymes are parsed


    Public Methods
    --------------
    parse( outputfile : path ) -> NetAcetData
        Parses the NetAcet prediction output file and add the data inside the
        above attribute data structure.

    submit_online (fastafile : Path, outputfile: Path)
        Submits online job. Provided as arguments are the input fasta file and the
        prediction output file paths

    """


    predicted_sites : dict


    @staticmethod
    def parse(outputfile: Path) -> Netacet_data:
        """Parses predictor's output"""

        predicted_sites = {}
        name = outputfile.name
        protname = name.split('.')[0]
        predicted_sites[protname] = {}

        try:
            f = open(outputfile, 'r')
            lines = f.readlines()
            if "Failed: Online job submission failed" in lines[0]:
                protname = (outputfile.name).split('.')[0]
                predicted_sites = {}
                predicted_sites[protname] = {}
                return Netacet_data(predicted_sites)

            for line in lines:
                l = line.split()
                if len(l) == 6 and l[0][0] not in '<#' :

                    aa = l[2]
                    start = int(l[1])
                    end = start
                    score = round(float(l[4]), 3)
                    is_signif = (l[5] == "YES")

                    resid = start

                    if resid not in predicted_sites[protname]:
                        predicted_sites[protname][resid] = []

                    predicted_sites[protname][resid].append({
                        "seq": aa,
                        "start": start,
                        "end": end,
                        "is_signif": is_signif,
                        "score": score,
                        "type": "Nter-acet",
                        "predictor": "netacet:1.0_online"
                    })

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        print(predicted_sites)
        return Netacet_data(predicted_sites)


    @staticmethod
    def submit_online (fastafile : Path, outputfile: Path) :
        """Submits online job. Provided as arguments are the input fasta file and the
            prediction output filename"""

        url = 'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi'

        #launch job

        f = FASTA()
        f.read_fasta(fastafile)
        seq = f.sequence

        data = {'SEQPASTE': seq, 'configfile':'/var/www/html/services/NetAcet-1.0/webface.cf'}

        try:
            r1 = requests.post(url, data=data)

            #retrieve results
            temp = re.search(r"jobid: .+ status", r1.text)
            jobid = temp.group().split(' ')[1]

            sleep(2)
            r2 = requests.get(url, params={'jobid' : jobid })

            count = 0; maxtime = 300
            while jobid in r2.text and count < maxtime/2:
                sleep(2)
                r2 = requests.get(url, params={'jobid': jobid })
                count +=1

            r2.raise_for_status()

            file = open(outputfile, "w")
            file.write(r2.text)

        except Exception as e:
            print("Failed: Online job submission failed !!!!")
            if hasattr(e, 'message'): print(e.message)
            else: print(e)
            with open(outputfile, 'w', encoding='utf-8') as f:
                print("#Failed: Online job submission failed !!!! Error: ", e, file=f)
            pass
