import click
from bioservices import *
from bioservices.apps import FASTA

from pathlib import Path
import sys, random

from glycosylation.GlycosylationPred import GlycosylationPred
from glycosylation.NetCglycData import NetCglycData
from glycosylation.NetOglycData import NetOglycData
from glycosylation.NetNglycData import NetNglycData
from glycosylation.GlycomineData import GlycomineData
from glycosylation.NGlyDEData import NGlyDEData


@click.group(chain=True, invoke_without_command=True)
def cli():
    pass


@cli.command()
@click.option('--uniprot', required=True, help='Id of the protein to fetch')
@click.option('--filename', required=False, help='filename to save')
def get_fasta(uniprot: str, filename: str = None):
    """Simple program that greets NAME for a total of COUNT times."""
    click.echo(f"receiving fasta sequence for uniprot id ${uniprot}")
    f: FASTA = FASTA()
    f.get_fasta(uniprot)  # bioservices use ugly mutable getters
    output = uniprot + ".fasta" if filename is None else (filename if ".fasta" in filename else filename + ".fasta")
    click.echo(f"saving protein fasta to ${output}")
    f.save_fasta(output)
    return output


@cli.command()
@click.option('--predictor', required=True, help='Name of the predictor to use')
@click.option('--input', required=True, help='Input fasta file path')
@click.option('--output', required=True, help='Output file')
@click.option('--type', required=False, help='Additional arguments to be passed; predictor specific')
def submitOnline(predictor: str, input: Path, output: Path, type: str = None):
    """Submit online jobs for a given predictor"""

    # Predictors that can be run online

    predictors = [
        # glycosylation
        'netcglyc', 'netnglyc', 'netoglyc', 'glycomine', 'nglyde'
    ]

    if predictor not in predictors:
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
@click.option('--formattype', required=True, help='"single" or "multi" protein layout')
@click.option('--module', required=False, help='prediction module; accepted values: all, structural, ptsmod, glycosylation, \
                phosphorylation, acetylation, sumoylation, localisation')
@click.option('--inputfolder', required=True, help='Input folder where all prediction results are stored')
@click.option('--output', required=True, help='Output formatted file')
@click.option('--signif', required=False, help='Print only significant predictions. Default: false')
@click.option('--protname', required=False, help='Only for single protein format, when within the specified input \
                folder there are multiple files with the same extension, a basename of the protein should be provided. \
                Example: protname.predictor.out; Default: null')
def formatoutput(formattype: str, module: str, inputfolder: Path, output: Path, signif: bool = False,
                 protname: str = None):
    """
        Format output according to their module
        For the moment it assumes that all prediction files are within the same file.
        Not all available options are yet implemented
    """
    if formattype == 'single':

        if module == 'glycosylation':

            keys = ["netnglyc", "nglyde", "glycomineN", "netoglyc", "isoglyp", "glycomineO", "netcglyc",
                               "glycomineC", "fasta", "fsa"]

            inputfolder=Path(inputfolder);
            paths = getPaths1prot(inputfolder, output, keys, protname);

            predictions = GlycosylationPred.parseall(paths)
            predictions.print1prot(outputFile=output, addseq=True, signif=signif)

        else:
            print("Not yet implemented...")
    else:
        print("Not yet implemented...")


def getPaths1prot(inputfolder: Path, output: Path, keys: list, protname: str = None) -> dict:
    paths = {};
    for key in keys:
        try:
            if protname is None:
                files = list(inputfolder.rglob('*.' + key + '*'))
            else:
                files = list(inputfolder.rglob(protname + '.' + key + '*'))

            if len(files) > 1:
                print("Multiple options: ", list)
                raise
            elif len(files) == 0:
                if (key == 'fasta'):
                    print("In the provided input folder there is no file with either the provided protname : '", protname, \
                      "' or predictor suffix: '", key, "' . Searching for *.fsa...", sep='')
                else:
                    print("In the provided input folder there is no file with either the provided protname : '", protname, \
                      "' or predictor suffix: '", key, "'.", sep='')
            else:
                if protname is None:
                      protname = files[0].name.split('.'+key)[0]
                      print("Within the provided folder, protname : '", protname, \
                      "' was found. Updating protname.", sep='')

                if protname not in paths:
                      paths[protname] = {}
                paths[protname][key] = files[0]

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    return paths


if __name__ == '__main__':
    cli()
