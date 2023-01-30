""" Wrapper module around the Candy Machine CLI tool """

from os import system
from os.path import abspath, exists
from shutil import which

from rich import print as log

# The Candy Machine version to be used
CM_VERSION = "v1.2.0"
# The URL at which the Candy Machine is available
CM_REPO_URL = "https://github.com/metaplex-foundation/metaplex.git"
# The path in which the Candy Machine CLI will be available
CM_OUT_PATH = abspath("./dependency/metaplex")
# The base command to be executed
CM_CLI_CMD = "ts-node ./dependency/metaplex/js/packages/cli/src/candy-machine-v2-cli.ts"
# The command for setting the keypair
CM_SOL_SET = "solana config set"

# ! <---------        MODULE INITIALIZATION CODE        ---------> ! #
# If the Candy Machine CLI is not installed, do it now
if not exists(CM_OUT_PATH):
    # Check for existence of the required binaries/commands
    assert which("git") is not None, "'git' must be installed on your computer"
    assert which("yarn") is not None, "'yarn' must be installed on your computer"
    assert which("solana") is not None, "'solana' must be installed on your computer"

    # Clones the repo at the specified version tag
    exit_status = system(f"git clone -b {CM_VERSION} {CM_REPO_URL} {CM_OUT_PATH}")
    assert exit_status == 0, "Candy Machine download failed"

    # Install NPM dependencies for the repo
    exit_status = system(f"yarn install --cwd {CM_OUT_PATH}/js")
    assert exit_status == 0, "Candy Machine dependency download failed"

    # Installs ts-node and typescript toolchain globally
    exit_status = system("yarn global add ts-node typescript")
    assert exit_status == 0, "ts-node installation failed, please fix"

# TODO ADD ts-node to the PATH variable every time the module is used
log("[yellow]Please check that ts-node is available in your PATH variable[/yellow]")
