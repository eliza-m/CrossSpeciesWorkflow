from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import sys
import requests
from bs4 import BeautifulSoup as bs


@dataclass
class Gpssumo_data:
    """Class that parses GpsSUMO prediction output data.

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
    parse( outputfile : path ) -> Gpspail_data
        Parses the GpsPail prediction output file and add the data inside the
        above attribute data structure.

    submit_online (fastafile : Path, outputfile: Path)
        Submits online job. Provided as arguments are the input fasta file and the
        prediction output file paths
H
    """

    predicted_sites: dict

    @staticmethod
    def parse(outputfile: Path) -> Gpssumo_data:

        predicted_sites = {}

        try:
            with open(outputfile, 'r', encoding='utf-8') as f:
                content = f.read()
                soup = bs(content, "html.parser")
                table = soup.find('table')
                rows = table.findAll('tr')

                for r in rows:
                    cols = r.findAll('td')
                    if len(cols) > 0 and cols[0].text :
                        protname = cols[0].text.split()[0]
                        longtype = cols[6].text
                        type = 'SIM' if 'Interaction' in longtype else 'SUMO' if 'Sumoylation' in longtype else 'unk'

                        if type == 'SIM':
                            range = cols[1].text.split('-')
                            start = int(range[0])
                            end = int(range[1])
                        else:
                            start = end = int(cols[1].text)

                        aa = cols[2].text[7:-7]
                        score = round(float(cols[3].text), 3)
                        cutoff = round(float(cols[4].text), 3)
                        pval = round(float(cols[5].text), 3)
                        is_signif = score >= cutoff

                        resid = start

                        if protname not in predicted_sites:
                            predicted_sites[protname] = {}

                        if resid not in predicted_sites[protname]:
                            predicted_sites[protname][resid] = []

                        predicted_sites[protname][resid].append({
                            "seq": aa,
                            "start": start,
                            "end": end,
                            "is_signif": is_signif,
                            "score": score,
                            "cutoff": cutoff,
                            "pval": pval,
                            "type": type,
                            "predictor": "gpssumo_online"
                        })

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return Gpssumo_data(predicted_sites)

    @staticmethod
    def submit_online(fastafile: Path, outputfile: Path):

        url1 = 'http://sumosp.biocuckoo.org/transfer.php'
        url2 = 'http://sumosp.biocuckoo.org/showResult.php'

        # launch job

        with open(fastafile, 'r') as f:
            seq = f.read()

        data = {
                'text': seq,
                'sum': 'Medium',
                'bin': 'Medium',
                'bool': 'on'
                }

        s = requests.Session()
        r1 = s.post(url1, data=data)

        # retrieve results
        r2 = s.get(url2)
        r2.raise_for_status()

        # html archive
        with open(outputfile, 'w', encoding='utf-8') as f:
            f.write(r2.text)

