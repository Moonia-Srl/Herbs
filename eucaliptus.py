"""
Herbs - Eucaliptus.py

This script allows to automate the transfer of multiple SPL token in the Solana blockchain.
The only required CLI argument is the path to a .csv files that contains the wallets and number
of token to be transferred and the collectionId/programId to retrieve all the tokens associated
to the Candy Machine.

! NOTE: In order for this script to work the Solana CLI must be installed and the
! keypair must be set globally with the following command:
!     $ solana config set --keypair ~/.config/solana/your_key.json

Example:
    $ python3 eucaliptus.py --collectionId="8gex...i895fei4" --csv=../mock.csv
"""

from csv import DictReader
from datetime import datetime
from functools import reduce
from itertools import repeat
from os import PathLike, system
from os.path import abspath, basename, exists, isfile
from random import choice
from shutil import which
from typing import List

from fire import Fire
from pydantic import BaseModel, PositiveInt
from rich.console import Console

from rarible import RaribleNFT
from rarible.items import get_by_owner

# The bash command format to be used in order to transfer SPL Tokens
TRANSFER_CMD = "spl-token transfer {token_addr} 1 {dest_addr} --allow-unfunded-recipient --fund-recipient"
# A shared/sharable console object to pretty print strings
console = Console(record=True)


class CsvRow(BaseModel):
    """The format required for the input .csv row"""
    address: str
    quantity: PositiveInt


def get_owned_by_collection(wallet: str, collection_id: str, env: str = "devnet") -> List[RaribleNFT]:
    """Returns a list of NFT from the given collection owned by the given wallet"""
    # Gets all the NFTs owned by the provided wallet
    owned_nfts = get_by_owner(wallet, env)
    # Filters out the one not coming/related to the provided collection
    filter_by_collection = lambda nft: nft.collection == f"SOLANA:{collection_id}"
    filtered_nfts: list[RaribleNFT] = [nft for nft in filter(filter_by_collection, owned_nfts)]

    # ! Debug only, will remove later
    console.print(f"[green]\n -> Owned NFTs from the specified collection (n. {len(filtered_nfts)})[/green]")
    [console.print(f"[yellow]\t{x.id} -> {x.meta.name}[yellow]") for x in filtered_nfts]

    return filtered_nfts


def get_transfers_list(csv_path: PathLike) -> List[CsvRow]:
    """Read the transfer .csv and returns a typed list if the format is correct"""
    # Reads input .csv file and converts it to a typed dataclass
    transfers_todo = [CsvRow(**row) for row in DictReader(open(csv_path, "r", encoding="utf-8"))]

    # ! Debug only, will remove later
    console.print(f"[green]\n -> Presale adn transfers to be made (n. {len(transfers_todo)})[/green]")
    [console.print(f"[yellow]\t{x.address} -> {x.quantity}[/yellow]") for x in transfers_todo]

    return transfers_todo


def main(wallet: str, collection_id: str, csv_path: PathLike, env: str = "devnet") -> None:
    """Lavender script entrypoint"""
    # Extracts the full path from filesystem root and the base url for Rarible API
    csv_abspath = abspath(csv_path)

    # Arguments and dependency checking
    assert exists(csv_abspath), f"{csv_abspath} not existing"
    assert isfile(csv_abspath), f"{csv_abspath} is not a file"
    assert which("spl-token") is not None, "'spl-token' command not found or not available"

    # The list of NFT from the given collection owned by us
    owned_collection_nfts = get_owned_by_collection(wallet, collection_id, env)
    # The transfer destinations and the amount of tokens to be transferred for each
    transfers_list = get_transfers_list(csv_abspath)

    # Aggregate value of the full amount of SPL token to be transferred
    n_transfers = reduce(lambda acc, t: acc + int(t.quantity), transfers_list, 0)

    assert n_transfers <= len(owned_collection_nfts), "More transfers required than token owned"

    # ! Debug only, will remove later
    console.print("[red]\n -> SPL token transfer log[/red]")

    # Transfers one token at time to all the wallets in the list
    for transfer in transfers_list:
        for _ in range(int(transfer.quantity)):
            # Chooses a NFT from the list and get its SPL token address from the token id
            # the list isn't sorted so the choice is always pseudo-random
            token_address = owned_collection_nfts.pop().id.split(":").pop()

            # Interpolates the bash command with the correct params
            fmt_map = {'token_addr': token_address, 'dest_addr': transfer.address}
            cmd = TRANSFER_CMD.format_map(fmt_map)

            # Runs the command in bash and returns a message based on the exit status
            if system(cmd) == 0:
                console.print(f"[green]SPL transfer {token_address} to {transfer.address} completed[/green]")
            else:
                console.print(f"[red]SPL transfer {token_address} to {transfer.address} failed[/red]")


# Eucaliptus script entrypoint, uses fire to generate CLI from function
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
