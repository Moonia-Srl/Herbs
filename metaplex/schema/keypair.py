from pydantic import BaseModel, conint, validator


class Keypair(BaseModel):
    """Validator class that checks the the JSON file with the user's keypair"""
    bytes: list[conint(gt=0, lt=256)]  # 64 byte long keypair

    @validator('bytes')
    def has_valid_length(cls, kp_bytes: list[int]):
        """Check if the 'bytes' field is exactly long 64 (the keypair must be 64 bytes)"""
        assert len(kp_bytes) == 64, "Invalid or wrong keypair length."
