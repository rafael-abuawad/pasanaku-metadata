import click
import os
from ape.cli import ConnectedProviderCommand
from ape import project, accounts
from dotenv import load_dotenv


load_dotenv()

ANVIL_CHAIN_ID = 31337


@click.command(cls=ConnectedProviderCommand)
def cli(ecosystem, network, provider):
    # Access chain and other managers automatically
    from ape import chain

    click.echo(f"Current chain id: {chain.chain_id}")

    deployer = accounts.load(os.getenv("DEPLOYER"))
    if chain.chain_id == ANVIL_CHAIN_ID:
        deployer.balance = int(100*10**18)

    layout_ended = project.LayoutEnded.deploy(sender=deployer)
    layout_ongoing = project.LayoutOngoing.deploy(sender=deployer)

    token_descriptor = project.TokenDescriptor.deploy(layout_ended.address, layout_ongoing.address, sender=deployer)
    return token_descriptor
