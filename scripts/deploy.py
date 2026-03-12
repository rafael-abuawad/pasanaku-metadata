import click
import os
from ape.cli import ConnectedProviderCommand
from ape import project, accounts
from dotenv import load_dotenv


load_dotenv()


@click.command(cls=ConnectedProviderCommand)
def cli(ecosystem, network, provider):

    # Access chain and other managers automatically
    from ape import chain

    click.echo(f"Current chain id: {chain.chain_id}")

    deployer = accounts.load(os.getenv("DEPLOYER"))
    token_descriptor = project.TokenDescriptor.deploy(sender=deployer)
    return token_descriptor
