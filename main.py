import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    SOCA (Software Catalog Creator)\n
    Automatically generates a searchable portal for every repository of an organization/s or user/s, which is easy to host.\n

    Usage:

    1. (fetch) Fetch all repos from the desired organization/s\n
    2. (extract) Extract all metadata for every repo\n
    3. (portal) Generate a searchable portal for all the retrieved data\n

    """
    pass

@cli.command()
@click.option('--input','-i', required=True, help="Organization or user name", metavar='<name-or-path>')
@click.option('--output','-o', default="repos.csv", show_default=True, help="Output csv file", metavar='<path>')
@click.option('--org', 'repo_type', flag_value='orgs', default=True, show_default=True, help="Extracting from a organization")
@click.option('--user', 'repo_type', flag_value='users', default=False, show_default=True, help="Extracting from a user")
@click.option('--not_archived','-na', flag_value=True, default=False, show_default=True, help="Fetch only repos that are not archived")
@click.option('--not_forked','-nf', flag_value=True, default=False, show_default=True, help="Fetch only repos that are not forked")
@click.option('--not_disabled','-nd', flag_value=True, default=False, show_default=True, help="Fetch only repos that are not disabled")
def fetch(input, output, repo_type, not_archived, not_forked, not_disabled):
    """Retrieve all organization/s or user/s repositories"""
    from soca.commands import fetch_repositories
    fetch_repositories.fetch(input, output, repo_type, not_archived, not_forked, not_disabled)


