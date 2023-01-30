""" Wrapper module around the Rarible Multichain API """

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, NonNegativeInt

RARIBLE_API = {
    "mainnet": "https://api.rarible.org/v0.1",
    "devnet": "https://testnet-api.rarible.org/v0.1",
}


class RaribleMetadata(BaseModel):
    """Validator class to type annotate the 'metadata' field in the RaribleNFT object"""
    name: str
    description: str
    tags: list[str]
    genres: list[str]

    # ? Not needed now =>  attributes: list[RaribleAttributes]
    # ? Not needed now =>  content: list[RaribleAsset]
    # ? Not needed now =>   restrictions: list[unknown]


class RaribleNFT(BaseModel):
    """Validator class to type annotate the NFTs data returned by Rarible API"""
    id: str
    collection: Optional[str] = None
    blockchain: Literal["ETHEREUM", "SOLANA", "POLYGON", "TEZOS"]

    meta: Optional[RaribleMetadata] = None

    mintedAt: datetime
    lastUpdatedAt: datetime

    deleted: bool
    supply: NonNegativeInt
    sellers: NonNegativeInt
    totalStock: NonNegativeInt
    lazySupply: NonNegativeInt

    # ? Not needed now => pending: list[unknown]
    # ? Not needed now => auctions: list[unknown]
    # ? Not needed now => creators: list[unknown]
    # ? Not needed now => originOrders: list[unknown]
