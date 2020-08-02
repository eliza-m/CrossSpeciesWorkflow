import click
from bioservices import *
from bioservices.apps import FASTA

@click.command()
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

if __name__ == '__main__':
    get_fasta()