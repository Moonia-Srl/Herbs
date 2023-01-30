"""
Herbs - Peppermint.py

This script allows to automate the minting process of an NFT collection using Metaplex's
Candy Machine implementation as well as the provided CLI interface for the latter.

! NOTE: In order for this script to work the Solana CLI must be installed.

! NOTE: The scripts expects and enforces a specific project structure for each Candy Machine
! the expected folder structure is the following:
! |
! |__ assets
! |   |_ Images and JSON metadata, number from 0 to X
! |__ config.json
! |   |_ Candy Machine configuration file (https://docs.metaplex.com/candy-machine-v2/configuration)
! |__ keypair.json
!     |_ The keypair used to deploy the CM and pay for the related fees

Example:
    $ python3 peppermint.py COMMAND ...ARGS
"""

from datetime import datetime
from os.path import basename

from fire import Fire
from rich.console import Console

from metaplex.deploy import deploy_nfts
from metaplex.post_deploy import mint, sign_all, withdraw_rent
from metaplex.verify import verify_project

# A shared/sharable console object to pretty print strings
console = Console(record=True)

# A list of all the available subcommands (each one of them has a specific 'scope')
subcommands = {
    # Pre deploy operations
    "verify": verify_project,
    # Deploy operations, uploads the assets & metadata, deploys the Candy Machine on chain
    "deploy": deploy_nfts,
    # Post deploy operations
    "mint": mint, "sign_all": sign_all, "withdraw_rent": withdraw_rent
}


# Peppermint script entrypoint, uses fire to generate CLI from function
if __name__ == "__main__":
    try:
        Fire(subcommands)
    except KeyboardInterrupt:
        console.print("[yellow]Interrupt received, closing now..[/yellow]")
    except Exception:
        console.print("[red]An unexpected error occurred[/red]")
        console.print_exception()
    finally:
        script_name = basename(__file__)
        current_date = datetime.now().strftime('%d-%m-%Y %H:%M')
        console.save_text(f"logs/{script_name} {current_date}.log", clear=False)
