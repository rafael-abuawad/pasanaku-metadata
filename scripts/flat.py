import click
from ape import compilers, project


def main():
    click.echo("Flattening contract...")
    source_path = project.TokenDescriptor.source_path
    click.echo(f"Source path: {source_path}")
    flattened_src = compilers.flatten_contract(source_path)
    click.echo("Flattened")
    with open("flattened/TokenDescriptor.sol", "w") as f:
        f.write(str(flattened_src))


if __name__ == "__main__":
    main()
