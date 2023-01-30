from datetime import datetime
from typing import Any, Literal, Optional

from base58 import b58decode
from pydantic import AnyUrl, BaseModel, PositiveFloat, PositiveInt, validator

# Decentralized storage providers supported by the Candy Machine CLI
StorageProvider = Literal[ \
    "aws", "ipfs", "pinata", "arweave", "nft-storage", "arweave-sol", "arweave-bundle" \
]


class Configuration(BaseModel):
    """Validator class that checks the the JSON file for the Candy Machine configuration"""
    number: PositiveInt  # The maximum number of max token available to be minted

    price: PositiveFloat  # The unit price for each NFT/token
    solTreasuryAccount: str  # The account that will receive the profits

    splToken: None  # SPL Tokens for which the Candy Machine can accept payment
    splTokenAccount: None  # Wallet that will receives aforesaid SPL tokens

    storage: StorageProvider  # The decentralized storage provider

    goLiveDate: str  # The date after which the public sale will begin
    noMutable: bool = False  # When True, disables consequent update on the metadata
    noRetainAuthority: bool = False  # Enables the transfer of Update Authority from CM to minter

    gatekeeper: Optional[Any] = None  # Enables Captcha verification to avoid bot minting
    endSettings: Optional[Any] = None  # Disables minting after a specific date or amount
    hiddenSettings: Optional[Any] = None  # Hidden Candy Machine settings
    whitelistMintSettings: Optional[Any] = None  # Settings for private sale/ whitelist minting

    pinataJwt: Optional[str] = None  # Pinata Storage auth token
    pinataGateway: Optional[AnyUrl] = None  # Pinata custom gateway URL

    awsS3Bucket: Optional[str] = None  # AWS S3 Bucket Name

    nftStorageKey: Optional[str] = None  # NFT Storage API key

    arweaveJwk: Optional[str] = None  # Arweawe JWK wallet file path

    ipfsInfuraProjectId: None  # Infura project ID
    ipfsInfuraSecret: None  # Infura project secrets

    @validator('solTreasuryAccount')
    def is_solana_addr(cls, value: str):
        """Check if the solTreasuryAccount field is a valid Solana address (base58 - 256 bit)"""
        assert len(b58decode(value)) == 32, "The provided value isn't a valid Solana address"

    @validator('goLiveDate')
    def is_valid_date(cls, value: str):
        """Check if the goLiveDate field is a valid date format"""
        assert datetime.strptime(value, '%d %b %Y %H:%M:%S %Z'), "Invalid date provided"

    @validator('storage')
    def is_valid_storage_cfg(cls, storage: StorageProvider, values: dict[str, str]):
        """Validate the storage configuration based on the selected storage provider"""
        match storage:
            case "aws":
                assert values["awsS3Bucket"] is not None, "awsS3Bucket must be defined"
            case "ipfs":
                assert values["ipfsInfuraSecret"] is not None, "ipfsInfuraSecret must be defined"
                assert values["ipfsInfuraProjectId"] is not None, "ipfsInfuraProjectId must be defined"
            case "pinata":
                assert values["pinataJwt"] is not None, "pinataJwt must be defined"
                assert values["pinataGateway"] is not None, "pinataGateway must be defined"
            case ("arweave" | "arweave-bundle"):
                assert values["arweaveJwk"] is not None, "arweaveJwk must be defined"
            case "nft-storage":
                assert values["nftStorageKey"] is not None, "nftStorageKey must be defined"
