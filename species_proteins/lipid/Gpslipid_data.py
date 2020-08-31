from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import sys
import requests
from bs4 import BeautifulSoup as bs


@dataclass
class Gpslipid_data:
    """Class that parses GpsLipid prediction output data.

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

    Public Methods
    --------------
    parse( outputfile : path ) -> Gpslipid_data
        Parses the prediction output file and add the data inside the
        above attribute data structure.

    submit_online (fastafile : Path, outputfile: Path)
        Submits online job. Provided as arguments are the input fasta file and the
        prediction output file paths
H
    """

    predicted_sites: dict

    @staticmethod
    def parse(outputfile: Path) -> Gpslipid_data:
        """Parses predictor's output"""

        predicted_sites = {}

        try:
            with open(outputfile, 'r', encoding='utf-8') as f:
                content = f.read()
                if "Failed: Online job submission failed" in content:
                    protname = (outputfile.name).split('.')[0]
                    predicted_sites[protname] = {}
                    return Gpslipid_data(predicted_sites)

                soup = bs(content, "html.parser")
                table = soup.find('tbody')
                rows = table.findAll('tr')

                for r in rows:
                    cols = r.findAll('td')
                    protname = cols[0].text.split()[0]
                    resid = int(cols[1].text)
                    aa = cols[2].text[7]
                    score = round(float(cols[3].text), 3)
                    cutoff = round(float(cols[4].text), 3)
                    type = cols[5].text.split()[0][0:5]

                    is_signif = score >= cutoff

                    if protname not in predicted_sites:
                        predicted_sites[protname] = {}

                    if resid not in predicted_sites[protname]:
                        predicted_sites[protname][resid] = []

                    predicted_sites[protname][resid].append({
                        "seq": aa,
                        "start": resid,
                        "end": resid,
                        "is_signif": is_signif,
                        "score": score,
                        "cutoff": cutoff,
                        "type": type,
                        "predictor": "gpslipid_online"
                    })

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return Gpslipid_data(predicted_sites)

    @staticmethod
    def submit_online(fastafile: Path, outputfile: Path):
        """Submits online job. Provided as arguments are the input fasta file and the
                        prediction output filename"""

        url1 = 'http://lipid.biocuckoo.org/coreExecute/convert.php'
        url2 = 'http://lipid.biocuckoo.org/presult.php'

        # launch job

        with open(fastafile, 'r') as f:
            seq = f.read()

        data = {
                'text': seq,
                'pal': 'pal',
                'myr': 'myr',
                'far': 'far',
                'ger': 'ger',
                'thresold': 'm'
                }
        try:
            s = requests.Session()
            r1 = s.post(url1, data=data)

            # retrieve results
            r2 = s.get(url2)
            r2.raise_for_status()

            # html archive
            with open(outputfile, 'w', encoding='utf-8') as f:
                f.write(r2.text)

        except Exception as e:
            print("Failed: Online job submission failed !!!!")
            if hasattr(e, 'message'): print(e.message)
            else: print(e)
            with open(outputfile, 'w', encoding='utf-8') as f:
                print("#Failed: Online job submission failed !!!! Error: ", e, file=f)
            pass



