from os import PathLike, system
from os.path import abspath, basename, join

from rich import print as log

from metaplex import CM_CLI_CMD


def withdraw_rent(cm_address: str, key_path: PathLike, env: str = "devnet") -> None:
    """
    Allow to withdraw rent from the Candy Machine and transfer the funds to the caller/owner.
    NOTE: This operation makes the Candy Machine unavailable for later usage, this means that
    operation such as NFT update, price changes cannot be performed anymore.
    """
    # Executes the shell command and asserts on the exit code to be a success
    cmd = f"{CM_CLI_CMD} withdraw {cm_address} -e {env} -k {abspath(key_path)}"
    assert system(cmd) == 0, "'Withdraw Rent' command failed"

    log(f"[green]Withdrawn rent successfully from CM {cm_address}[/green]")


def sign_all(project_path: PathLike, env: str = "devnet") -> None:
    """
    Allow to sign all the NFTs deployed for the given project Candy Machine.
    """
    # Derives the needed data/file from project path
    key_abspath, project_name = join(abspath(project_path), "keypair.json"), basename(project_path)

    # Executes the shell command and asserts on the exit code to be a success
    cmd = f"{CM_CLI_CMD} sign_all -e {env} -k {key_abspath} -c {project_name}"
    assert system(cmd) == 0, "'Sign All' command failed"

    log("[green]All NFTs signed successfully[/green]")


def mint(project_path: PathLike, num: int = 1, env: str = "devnet") -> None:
    """
    Allow to mint one or more token for the given project Candy Machine.
    """
    # Derives the needed data/file from project path
    key_abspath, project_name = join(abspath(project_path), "keypair.json"), basename(project_path)

    # Executes the shell command and asserts on the exit code to be a success
    cmd = f"{CM_CLI_CMD} mint_multiple_tokens -e {env} -k {key_abspath} -c {project_name} --number {num}"
    assert system(cmd) == 0, "Minting command failed"

    log(f"[green]{num} NFTs successfully minted[/green]")
