"""
Herbs - Lavender.py

This script allows to automate the purge of all the NFTs owned by a Solana wallet.
It determines the SPL token detained via the Solana CLI tool and proceeds with the purge
of all the detained tokens.

! NOTE: In order for this script to work the Solana CLI must be installed and the
! keypair must be set globally with the following command:
!     $ solana config set --keypair ~/.config/solana/your_key.json

Example:
    $ python3 lavender.py
"""

from datetime import datetime
from json import loads
from os import system
from os.path import basename
from shutil import which
from subprocess import run

from fire import Fire
from rich.console import Console


# The bash command to be used in order to get a JSON array of the owned SPL tokens
LIST_SPL_CMD = "spl-token accounts -v --output json"
# The bash command format to be used in order to burn SPL Tokens
BURN_SPL_CMD = "spl-token burn {account} {quantity}"
# The bash command format to close an account and withdraw its rent
CLOSE_ACC_CMD = "spl-token close {token}"
# A shared/sharable console object to pretty print strings
console = Console(record=True)


def main() -> None:
    """Lavender script entrypoint"""
    # Arguments and dependency checking
    assert which("spl-token") is not None, "'spl-token' command not found or not available"

    status = run(LIST_SPL_CMD.split(), check=False, capture_output=True)
    assert status.returncode == 0, "'spl-token accounts' command execution failed"

    spl_token_list = loads(status.stdout)["accounts"]

    # Burns one token at time until all NFTs are purged
    for spl_token in spl_token_list:
        fmt_map = {
            "account": spl_token["address"],
            "quantity": spl_token["tokenAmount"]["amount"],
            "token": spl_token["mint"]
        }
        # Burns the current SPL token (transfers it to a burn address)
        burn_status = system(BURN_SPL_CMD.format_map(fmt_map))
        # Closes the related data account withdrawing the remaining rent
        close_status = system(CLOSE_ACC_CMD.format_map(fmt_map))

        if burn_status == 0 and close_status == 0:
            console.print(f"[green]Successfully purged token {spl_token['address']}[/green]")
        else:
            console.print(f"[red]Error during purge of token {spl_token['address']}[/red]")


# Lavender script entrypoint, uses fire to generate CLI from function
if __name__ == "__main__":
    try:
        Fire(main)
    except KeyboardInterrupt:
        console.print("[yellow]Interrupt received, closing now..[/yellow]")
    except Exception:
        console.print("[red]An unexpected error occurred[/red]")
        console.print_exception()
    finally:
        script_name = basename(__file__)
        current_date = datetime.now().strftime('%d-%m-%Y %H:%M')
        console.save_text(f"logs/{script_name} {current_date}.log", clear=False)
