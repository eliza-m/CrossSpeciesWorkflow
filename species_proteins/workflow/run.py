import click
from bioservices import *
from bioservices.apps import FASTA

from pathlib import Path

from glycosylation.GlycosylationPred import *
from glycosylation.NetCglycData import NetCglycData
from glycosylation.NetOglycData import NetOglycData
from glycosylation.NetNglycData import NetNglycData
from glycosylation.GlycomineData import GlycomineData
from glycosylation.NGlyDEData import NGlyDEData



@click.group(chain=True, invoke_without_command=True)
def cli():
    pass

@cli.command()
@click.option('--uniprot', required=True,  help='Id of the protein to fetch')
@click.option('--filename', required=False, help='filename to save')
def get_fasta(uniprot: str, filename: str = None):
    """Simple program that greets NAME for a total of COUNT times."""
    click.echo(f"receiving fasta sequence for uniprot id ${uniprot}")
    f: FASTA = FASTA()
    f.get_fasta(uniprot) # bioservices use ugly mutable getters
    output = uniprot + ".fasta" if filename is None else (filename if ".fasta" in filename else filename+".fasta")
    click.echo(f"saving protein fasta to ${output}")
    f.save_fasta(output)
    return output




@cli.command()
@click.option('--predictor', required=True,  help='Name of the predictor to use')
@click.option('--input', required=True, help='Input fasta file path')
@click.option('--output', required=True, help='Output file')
@click.option('--type', required=False, help='Additional arguments to be passed; predictor specific')
def submitOnline (predictor: str, input : Path, output: Path, type: str = None):
    """Submit online jobs for a given predictor"""

    # Predictors that can be run online

    predictors = [
                # glycosylation
               'netcglyc', 'netnglyc', 'netoglyc', 'glycomine', 'nglyde'
                ]

    if predictor not in predictors :
        print("Unknown predictor key: ", predictor)
        print("Try one of the following :\n", predictors)
        raise

    elif predictor == 'netcglyc':
        NetCglycData.submitOnline(input, output)

    elif predictor == 'netoglyc':
        NetOglycData.submitOnline(input, output)

    elif predictor == 'netnglyc':
        NetNglycData.submitOnline(input, output)

    elif predictor == 'glycomine':
        if type not in "NOC":
            print("Glycomine requires selecting a type: 'N', 'C' or 'O' for N/O/C-linked glycosylation prediction")
            raise
        GlycomineData.submitOnline(input, output, type)

    elif predictor == 'nglyde':
        NGlyDEData.submitOnline(input, output)




@cli.command()
@click.option('--formattype', required=True,  help='"single" or "multi" protein layout')
@click.option('--module', required=False, help='prediction module; accepted values: all, structural, ptsmod, glycosylation, \
					phosphorylation, acetylation, sumoylation, localisation')
@click.option('--inputfolder', required=True, help='Input folder where all prediction results are stored')
@click.option('--output', required=True, help='Output formatted file')

def formatoutput(formattype: str, module: str, inputfolder : Path, output: Path):
    """Format output according to their module"""
	




if __name__ == '__main__':
    cli()







