from os import PathLike, remove, system
from os.path import abspath, basename, join

from genericpath import exists, isfile
from rich import print as log

from metaplex import CM_CLI_CMD

# Path to the output log file
LOG_FILE_PATH = "./upload.log"


def deploy_nfts(project_path: PathLike, env: str = "devnet") -> None:
    """
    Aggregate function that handles assets and metadata upload, in particular:
    - Uploads assets and JSON to a decentralized storage provider.
    - Extracts the mint address from stdout for later usage.
    - Verifies the upload of the assets before returning.
    """
    # Uploads the images and metadata to storage
    mint_address = upload(project_path, env)
    log(f"[green]The collection mint address is: {mint_address}[/green]")

    # Verifies the upload before proceeding with the collection step
    verify_upload(project_path, env)
    log("[green]Upload verification completed successfully[/green]")

    # Sets the collection for all uploaded/deployed NFTs
    set_collection(mint_address, project_path, env)
    log("[green]Collection set for all the NFTs[/green]")


def upload(project_path: PathLike, env: str = "devnet") -> str:
    """
    Uploads the asset with Metaplex Candy Machine CLI.
    Extracts as well the mint address from stdout output log.
    """
    # Determines the full absolute path from root
    project_abspath = abspath(project_path)

    # Destination blockchain (testnet, devnet, mainnet)
    net = env
    # Extracts the project name (used for caching purposes)
    project = basename(project_path)
    # Computes the subfolder path from the root/project one
    assets = join(project_abspath, "assets")
    keypair = join(project_abspath, "keypair.json")
    config = join(project_abspath, "config.json")

    # Executes the shell command that upload all the assets to the specified storage provider
    cmd = f"{CM_CLI_CMD} upload -e {net} -k {keypair} -cp {config} -c {project} {assets}"
    # Asserts the exit status code to be success
    assert system(f"{cmd} > {LOG_FILE_PATH}") == 0, "Upload command has failed"
    # Asserts the existence of the log file with the upload cmd output
    assert exists(LOG_FILE_PATH), "Upload log file not created"
    assert isfile(LOG_FILE_PATH), "Upload log file isn't a file"

    for out_line in open(LOG_FILE_PATH, "r", encoding="utf-8").readlines():
        if 'Collection mint address' in out_line:
            # Removes the log file from the cwd
            remove(LOG_FILE_PATH)
            # Extracts from the line the mint address of the Candy Machine
            return out_line.split(":")[1].lstrip()


def verify_upload(project_path: PathLike, env: str = "devnet") -> str:
    """
    Uses Metaplex's Candy Machine CLI to verify and check the upload correctness.
    """
    # Determines the full absolute path from root
    project_abspath = abspath(project_path)

    # Extracts the needed param from the project path
    project_name, keypair_path = basename(project_path), join(project_abspath, "keypair.json")

    # Executes the shell command and asserts on the exit code to be a success
    exit_status = system(f"{CM_CLI_CMD} verify_upload -e {env} -k {keypair_path} -c {project_name}")
    assert exit_status == 0, "Upload verification failed"


def set_collection(mint_address: str, project_path: PathLike, env: str = "devnet") -> None:
    """
    Sets the 'mint_address' collection for the uploaded/deployed NFTs.
    NOTE: This uses the project cache and not the assets folder, please do not remove it.
    """
    # Determines the full absolute path from root
    project_abspath = abspath(project_path)

    # Extracts the needed param from the project path
    project_name, keypair_path = basename(project_path), join(project_abspath, "keypair.json")

    # Executes the shell command and asserts on the exit code to be a success
    cmd = f"{CM_CLI_CMD} set_collection -e {env} -k {keypair_path} -c {project_name} -m {mint_address}"
    assert system(cmd) == 0, "upload command failed"
