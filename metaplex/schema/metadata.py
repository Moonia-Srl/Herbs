from typing import Optional, Union

from base58 import b58decode
from pydantic import BaseModel, PositiveInt, constr, validator


class Attribute(BaseModel):
    """Validator class that checks for correctness in NFT traits/attributes field"""
    trait_type: str
    value: Union[str, int, float]


class Creator(BaseModel):
    """Validator class that checks for correctness in NFT 'creators' field"""
    address: str  # The public address of the owner
    share: PositiveInt  # His share percentage (10 equals to 10%)

    @validator('address')
    def is_solana_addr(cls, value: str):
        """Check if the 'address' field is a valid Solana address (base58 - 256 bit)"""
        assert len(b58decode(value)) == 32, "The provided value isn't a valid Solana address"


class File(BaseModel):
    """Validator class that checks for correctness in NFT 'files' field"""
    uri: str  # The path to the resource/asset
    type: str  # The content type: "image/png", "application/json", ...


class Properties(BaseModel):
    """Validator class that checks for correctness in NFT 'properties' field"""
    creators: list[Creator]  # The NFT project founder/owner and their share
    files: list[File]  # The assets associated to the NFT

    @validator('creators')
    def check_percentages(cls, creators: list[Creator]):
        """Check if the shares expressed in 'properties' adds up to 100%"""
        total_percentage = sum([c.share for c in creators])
        assert len(creators) <= 4, "Too many creators specified (max 4)"
        assert total_percentage == 100, "Creators percentages are invalid"


class Collection(BaseModel):
    """Validator class that checks for correctness in NFT 'collection' field"""
    name: str  # The NFT collection name
    family: str  # The NFT collection full name


class Metadata(BaseModel):
    """Validator class that checks the the JSON file for the NFT metadata"""
    name: constr(min_length=1, max_length=32)  # Name of the NFT

    description: str  # A brief description about the project and/or collection
    symbol: constr(min_length=1, max_length=10)  # The collection's symbol

    # Percentage of royalties received from each selling
    seller_fee_basis_points: Optional[PositiveInt] = None

    image: constr(max_length=200)  # The asset (image, 3d model, ...) associated to the NFT
    attributes: list[Attribute]  # Lists of attributes/traits for the NFT

    properties: Properties  # It normally includes the creators and their percentage of royalties
    collection: Collection  # Name and family of the collection
