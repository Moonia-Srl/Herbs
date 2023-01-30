from json import load as json2dict
from os import PathLike, getcwd, listdir, system
from os.path import abspath, exists, isdir, isfile, join
from pathlib import Path

from rich import print as log

from metaplex import CM_CLI_CMD
from metaplex.schema.configuration import Configuration
from metaplex.schema.keypair import Keypair
from metaplex.schema.metadata import Metadata


def verify_project(project_path: PathLike) -> PathLike:
    """
    Executes a full verification of the given project folder, in particular:
    - Validates the JSON configuration file
    - Verifies the project folder structure
    - Checks that the number of assets and metadata file matches
    - Validate each single metadata JSON file
    """
    # Determines the full absolute path from root
    project_abspath = abspath(project_path)

    # Basic assertion and validations
    assert exists(project_abspath), f"{project_path} does not exists"
    assert isdir(project_abspath), f"{project_path} is not a directory"

    # Folder/file specific checks and validations
    verify_assets(join(project_abspath, "assets"))
    verify_metadata(join(project_abspath, "assets"))
    verify_keypair(join(project_abspath, "keypair.json"))
    verify_configuration(join(project_abspath, "config.json"))

    log("[green]Everything passed verification[/green]")


def verify_configuration(config_path: PathLike) -> None:
    """
    Checks that at least the minimal configuration has been provided.
    """
    # Determines the full absolute path from root
    config_abspath = abspath(config_path)

    # Basic assertion and validations
    assert exists(config_abspath), f"{config_path} doesn't exists"
    assert isfile(config_abspath), f"{config_path} isn't a file"

    # This one fails if the JSON provided isn' compliant with the Config schema
    Configuration(**json2dict(open(config_abspath, "r", encoding="UTF-8")))


def verify_assets(assets_path: PathLike) -> None:
    """
    Uses the Candy Machine CLI to verify the correctness of assets and metadata.
    Asserts before execution that the given directory exist and is not empty.
    """
    # Determines the full absolute path from root
    assets_abspath = abspath(assets_path)

    # Basic assertion and validations
    assert exists(assets_abspath), f"{assets_path} doesn't exists"
    assert isdir(assets_abspath), f"{assets_path} isn't a directory"
    assert len(listdir(assets_abspath)) != 0, f"{assets_path} is an empty directory"

    # Executes the shell command
    exit_status = system(f"{CM_CLI_CMD} verify_assets {assets_abspath.replace(getcwd(), '.')}")
    assert exit_status == 0, "Verification command failed"


def verify_keypair(keypair_path: PathLike):
    """
    Checks that the keypair provided is valid and well-formed.
    """
    # Determines the full absolute path from root
    keypair_abspath = abspath(keypair_path)

    # Basic assertion and validations
    assert exists(keypair_abspath), f"{keypair_abspath} doesn't exists"
    assert isfile(keypair_abspath), f"{keypair_abspath} isn't a file"
    assert Path(keypair_abspath).suffix == ".json", f"{keypair_abspath} isn't a JSON file"

    # This one fails if the JSON provided isn' compliant with the Config schema
    Keypair(bytes=json2dict(open(keypair_abspath, "r", encoding="UTF-8")))


def verify_metadata(assets_path: PathLike):
    """
    For each JSON files in the {project}/assets folder, checks that the
    metadata is well formed and conforms to the provided Meta schema.
    """
    # Determines the full absolute path from root
    assets_abspath = abspath(assets_path)

    # Inline function to filter out the JSON/metadata files
    filter_json = lambda file: Path(join(assets_abspath, file)).suffix == ".json"

    # Iterates over the metadata files in assets folder and validates each of them
    for file_metadata in filter(filter_json, listdir(assets_abspath)):
        metadata_abspath = join(assets_abspath, file_metadata)
        Metadata(**json2dict(open(metadata_abspath, "r", encoding="UTF-8")))
