import click
from bioservices.apps import FASTA

from species_proteins.util.util import *
from species_proteins.glycosylation.Glycosylation_pred import Glycosylation_pred
from species_proteins.glycosylation.Netcglyc_data import Netcglyc_data
from species_proteins.glycosylation.Netoglyc_data import Netoglyc_data
from species_proteins.glycosylation.Netnglyc_data import Netnglyc_data
from species_proteins.glycosylation.Glycomine_data import Glycomine_data
from species_proteins.glycosylation.Nglyde_data import Nglyde_data

from species_proteins.acetylation.Acetylation_pred import Acetylation_pred
from species_proteins.acetylation.Gpspail_data import Gpspail_data
from species_proteins.acetylation.Netacet_data import Netacet_data

from species_proteins.phosphorylation.Phosphorylation_pred import Phosphorylation_pred
from species_proteins.phosphorylation.Netphos_data import Netphos_data
from species_proteins.phosphorylation.Netphospan_data import Netphospan_data

from species_proteins.lipid.Lipid_pred import Lipid_pred
from species_proteins.lipid.Gpslipid_data import Gpslipid_data

from species_proteins.sumoylation.Sumoylation_pred import Sumoylation_pred
from species_proteins.sumoylation.Sumogo_data import Sumogo_data
from species_proteins.sumoylation.Gpssumo_data import Gpssumo_data



@click.group(chain=True, invoke_without_command=True)
def cli():
    pass


@cli.command()
@click.option('--uniprot', required=True, help='Uniprot ID to fetch')
@click.option('--filename', required=False, help='Filename to save. Default $id.fasta')
@click.option('--trimheader', is_flag=True, default=False, show_default=True, required=False, help='Trimm header to contain only id')
@click.option('--mode', default='w', show_default=True, required=False, help='Write("w") or append("a") mode')
def get_fasta(uniprot: str, filename: str = None, trimheader: bool = False, mode: str = 'w'):
    """Retrieves fasta file from UniprotKB ID"""
    click.echo(f"receiving fasta sequence for uniprot id ${uniprot}")
    f: FASTA = FASTA()
    f.load(uniprot)  # bioservices use ugly mutable getters

    if mode == "a":
        output = "prot.fasta" if filename is None else (filename if ".fasta" in filename else filename + ".fasta")
    else:
        output = uniprot + ".fasta" if filename is None else (
            filename if ".fasta" in filename else filename + ".fasta")

    newheader = f.header if trimheader is False else '>' + uniprot

    # Some predictors are more demanding with the fasta format...
    # Such as not accepting '\n', oddly parsing the UKB headers, spaces, etc...
    click.echo(f"saving protein fasta to ${output}")
    with open(output, mode) as file:
        print(newheader, sep='', file=file)
        print(f.sequence, file=file)



@cli.command()
@click.option('--input', required=True, help='Input FASTA file ')
@click.option('--output', required=True, help='Output filename')
@click.option('--predictor', required=True, help="""\b
                          Online predictor to submit sequence to. Predictors list per categories : 
                          - Glycosilation: 'netcglyc', 'netnglyc', 'netoglyc', 'glycomine', 'nglyde'
                          - Acetylation: 'netacet', 'gpspail'
                          - Phosphorylation: 'netphos', 'netphospan'
                          - Lipid modification: 'gpslipid'
                          - Sumoylation: 'gpssumo', 'sumogo'
                          - Cellular localisation: 'tmhmm'""")
def submit_online(predictor: str, input: Path, output: Path):

    """Submit online jobs for a given predictor"""

    # Predictors that can be run online
    predictors = [
        # glycosylation
        'netcglyc', 'netnglyc', 'netoglyc', 'glycomine', 'nglyde',
        # acetylation
        'netacet', 'gpspail',
        # phosphorylation
        'netphos', 'netphospan',
        # lipid
        'gpslipid',
        # Sumoylation
        'gpssumo', 'sumogo'
    ]

    if predictor not in predictors:
        print("Unknown predictor key: ", predictor)
        print("Try one of the following :\n", predictors)
        raise

    # GLYCOSYLATION
    elif predictor == 'netcglyc':
        Netcglyc_data.submit_online(input, output)
    elif predictor == 'netoglyc':
        Netoglyc_data.submit_online(input, output)
    elif predictor == 'netnglyc':
        Netnglyc_data.submit_online(input, output)
    elif predictor == 'nglyde':
        Nglyde_data.submit_online(input, output)
    elif predictor == 'glycomine':
        if type not in "NOC":
            print("Glycomine requires selecting a type: 'N', 'C' or 'O' for N/O/C-linked glycosylation prediction")
            raise
        Glycomine_data.submit_online(input, output, type)

    # ACETYLATION
    elif predictor == 'netacet':
        Netacet_data.submit_online(input, output)
    elif predictor == 'gpspail':
        Gpspail_data.submit_online(input, output)

    # PHOSPHORYLATION
    elif predictor == 'netphos':
        Netphos_data.submit_online(input, output)
    elif predictor == 'netphospan':
        Netphospan_data.submit_online(input, output)

    # LIPID MODIFICATION
    elif predictor == 'gpslipid':
        Gpslipid_data.submit_online(input, output)

    # SUMOYLATION
    elif predictor == 'sumogo':
        Sumogo_data.submit_online(input, output)
    elif predictor == 'gpssumo':
        Gpssumo_data.submit_online(input, output)



@cli.command()
@click.option('--format', required=True, help='"single" or "multi" protein layout')
@click.option('--module', required=True, help="""\b
                                Prediction module - accepted values: 
                                - all            :  All modules 
                                - all_nonstruct  :  All except structural module (which is slow) 
                                - ptsmod         :  All Post Translation modifications ( glyc + acet + phos + sumo + lipid) 
                                - struct         :  Structural module 
                                - glyc           :  Glycosylation module
                                - phos           :  Phosphorylation module
                                - acet           :  Acetylation module
                                - lipid          :  Lipid modification module
                                - sumo           :  Sumoylation module
                                - loc            :  Cellular localisation module """ )
@click.option('--inputfolder', required=True, help='Input folder where all prediction results are stored')
@click.option('--output', required=True, help='Output formatted file')
@click.option('--signif', is_flag=True, default=False, required=False, show_default=True, help='Print only significant predicted sites. It applies only for PTS predictors (significance thresholds are method specific.)')
@click.option('--protname', required=False, help="""\b
                Only for single protein format, when within the specified input
                folder there are multiple files with the same extension, a basename of the protein should be provided.
                Example: protname.predictor.out; Default: null""")
@click.option('--alnfile', required=False, help='Required for "multi" protein layout.')
def format_output(format: str, module: str, inputfolder: Path, output: Path, signif: bool = False,
                 protname: str = None, alnfile: Path = None):
    """
        Generates a vertical formatted layout of all predicted outputs. If 'multi' protein format is selected, sequences are shown aligned.
    """

    keys = {
        'glyc' : ["netnglyc", "nglyde", "glycomineN", "netoglyc", "isoglyp", "glycomineO", "netcglyc",
            "glycomineC", "fasta", "fsa"],
        'acet': ["netacet", "gpspail", "fasta", "fsa"],
        'phos': ["netphos", "netphospan", "musitedeepY", "musitedeepST", "fasta", "fsa"],
        'lipid': ["gpslipid", "fasta", "fsa"],
        'sumo': ["sumogo", "gpssumo", "fasta", "fsa"]
    }

    inputfolder = Path(inputfolder);

    if module not in keys:
        print("Unknown module or ...Not yet implemented...")
        raise

    if format == 'single':
        paths = get_paths_1prot(inputfolder, output, keys[module], protname);

    elif format == 'multi':
        if alnfile is None:
            print('Please provide alignment file for multi protrein layout')
        if module in keys:
            paths = get_paths_Nprot(inputfolder, output, keys[module]);

    else:
        print("Unknown format...")
        raise

    print("The following files will be parsed: ")
    for prot in paths:
        for f in paths[prot]:
            print(paths[prot][f])

        if     module == 'glyc': predictions = Glycosylation_pred.parse_all(paths)
        elif   module == 'acet': predictions = Acetylation_pred.parse_all(paths)
        elif   module == 'phos': predictions = Phosphorylation_pred.parse_all(paths)
        elif   module == 'lipid': predictions = Lipid_pred.parse_all(paths)
        elif   module == 'sumo': predictions = Sumoylation_pred.parse_all(paths)
        # elif   module == 'loc':  predictions = Localisation_pred.parse_all(paths)



        if format == 'single':
            predictions.print_1prot(outputfile=output, addseq=True, signif=signif)
        else:
            predictions.print_Nprot(outputfile=output, addseq=True, signif=signif, alnfile=alnfile)


if __name__ == '__main__':
    cli()
