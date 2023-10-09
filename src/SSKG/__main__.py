#TODO find appropiate names
import click
import os
from . import __version__
from .object_creator.create_downloadedObj import doi_to_downloadedJson, dois_txt_to_downloadedJson
from .object_creator.downloaded_to_paperObj import dwnlddJson_to_paperJson
from .object_creator.pipeline import dois_txt_to_unidir_json, dois_txt_to_bidir_json, pipeline_single_unidir, \
    pipeline_single_bidir

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
VALID_EXTENSIONS = ['.txt', '.json']


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__)
def cli():
    """
    ███████  ███████  ██   ██   ██████  \n
    ██       ██       ██  ██   ██       \n
    ███████  ███████  █████    ██   ███ \n
         ██       ██  ██  ██   ██    ██ \n
    ███████  ███████  ██   ██   ██████  \n

    Scientific Software Knowledge Graphs (SSKG)\n
    Automatically generates a searchable portal for every repository of an organization/s or user/s, which is easy to host.\n

    Usage:\n
    1. (assess)     Assess doi for unidirectionality or bidirectionality\n
    2. (download)   Download PDF (paper) from a doi or list\n
    3. (process)    Process downloaded pdf to find urls and abstract\n
    4. (summary)    Create a summary from the portal information

    """
    pass

# #TODO
# @cli.command()
# def configure():
#     """This creates a ~/.soca/configure.ini file"""
#     #TODO defaults check
#     url = click.prompt("URL to database",default = "http://localhost:8086")
#     bucket = click.prompt("Bucket", default = "my-bucket")
#     org = click.prompt("Organisation",default = "org_name")
#     token = click.prompt("Token", default = "")
#     if len(token) == 0:
#         click.echo("No token given, please enter token or press enter")
#         token = click.prompt("Token", default = "")
#     try:
#         from soca.commands import create_config
#
#         create_config.create_config(url,bucket,token,org)
#         click.secho(f"Success", fg="green")
#     except Exception as e:
#         click.secho(f"Error: "+str(e),fg="red")
#         exit(1)

@cli.command()
@click.option('--input','-i', required=True, help="DOI or path to .txt list of DOIs", metavar='<name>')
@click.option('--output','-o', default="output", show_default=True, help="Output csv file", metavar='<path>')
@click.option('--unidir', '-U', is_flag=True, default = False, help="Unidirectionality")
@click.option('--bidir', '-B', is_flag=True, default = False, help="Bidirectionality")
def assess(input, output,unidir,bidir):
    if unidir:
        if input.endswith(".txt") and os.path.exists(input):
            dois_txt_to_unidir_json(dois_txt=input,output_dir=output)
        if input.endswith(".json") and os.path.exists(input):
            return
        else:
            pipeline_single_unidir(doi=input,output_dir=output)
            return

    elif bidir:
        if input.endswith(".txt") and os.path.exists(input):
            print("test")
            dois_txt_to_bidir_json(dois_txt=input,output_dir=output)
        if input.endswith(".json") and os.path.exists(input):
            return
        else:
            pipeline_single_bidir(doi=input,output_dir=output)
            return
    else:
        print("Please select a directionality to measure")
        print("-U is to assess Uni-directionality")
        print("-B is to assess Bi-directionality")
    pass



@cli.command()
@click.option('--input','-i', required=True, help="DOI or path to .txt list of DOIs", metavar='<name>')
@click.option('--output','-o', default="./", show_default=True, help="Output Directory ", metavar='<path>')
def download(input, output):

    if input.endswith(".txt") and os.path.exists(input):
        dois_txt_to_downloadedJson(dois_txt=input, output_dir=output)
    else:
        try:
            doi_to_downloadedJson(doi=input, output_dir=output)
        except Exception as e:
            print(e)
        return
@cli.command()
@click.option('--input','-i', required=True, help="DOI or path to .txt list of DOIs", metavar='<name>')
@click.option('--output','-o', default="./", show_default=True, help="Output Directory ", metavar='<path>')
def process(input,output):
    if input.endswith(".json") and os.path.exists(input):
        dwnlddJson_to_paperJson(input,output)
    else:
        print("Error")
        return
    return

