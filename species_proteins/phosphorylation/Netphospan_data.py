from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import sys
import re
import requests
from time import sleep

@dataclass
class Netphospan_data:
    """Class that parses Netphospan prediction output data.

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
            score : float (probability)
            type : string
            predictor : string (for cases where multiple predictors are available)

        # Additional fields:
            enzyme: predictions for multple enzymes are parsed


    Public Methods
    --------------
    parse( outputfile : path ) -> Netphospan_data
        Parses the prediction output file and add the data inside the
        above attribute data structure.

    submit_online (fastafile : Path, outputfile: Path)
        Submits online job. Provided as arguments are the input fasta file and the
        prediction output file paths

    """

    predicted_sites : dict

    @staticmethod
    def parse(outputfile: Path) -> Netphospan_data :
        """Parses predictor's output"""

        predicted_sites = {}

        try:
            f = open(outputfile, 'r')

            lines = f.readlines()
            if "Failed: Online job submission failed" in lines[0]:
                protname = (outputfile.name).split('.')[0]
                predicted_sites[protname] = {}
                return Netphospan_data(predicted_sites)

            if lines[0][0] == "<":
                predictor = "netphospan:1.0_online"
            else : predictor = "netphospan:1.0_local"

            for line in lines:
                l = line.split()
                if len(l) == 5 and l[0]!='pos' and l[0][0] not in '#<' :

                    protname = l[3]
                    if protname not in predicted_sites:
                        predicted_sites[protname] = {}

                    peptide = l[2]
                    peplen = len(peptide)
                    aa = peptide[ int(peplen/2) ]

                    resid = int(l[0]) + 10
                    score = round(float(l[4]), 3)

                    is_signif = (score >= 0.5)
                    enzyme = 'general' if l[1]=="GENERIC" else 'kinase'

                    if resid not in predicted_sites[protname]:
                        predicted_sites[protname][resid] = []

                    predicted_sites[protname][resid].append({
                        "seq": aa,
                        "start": resid,
                        "end": resid,
                        "is_signif": is_signif,
                        "score": score,
                        "type" : aa + "-phosph",
                        "enzyme": enzyme,
                        "predictor": predictor
                    })


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return Netphospan_data(predicted_sites)



    @staticmethod
    def submit_online (fastafile : Path, outputfile: Path) :
    #  Only generic prediction is implemented yet

        try:

            url = 'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi'

            #launch job
            files = {'SEQSUB': open(fastafile, 'r')}
            data = {
                    'configfile':'/var/www/html/services/NetPhospan-1.0/webface.cf',
                    'generic_web':'1',
                    'master':'1'
                    }
            r1 = requests.post(url, data=data, files=files)

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


