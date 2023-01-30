""" Wrapper module around the Rarible Multichain API """

from requests import get

from rarible import RARIBLE_API, RaribleNFT


def get_by_owner(wallet: str, env: str = "devnet") -> list[RaribleNFT]:
    """ Get the NFTs owned by the given Solana wallet """
    # Initializes needed fields for later use
    base_url, nfts, session = RARIBLE_API.get(env, None), [], ""

    if base_url is None or not base_url:
        raise ValueError(f"env argument: '{env}' is not supported")

    while True:
        # Initializes the query param for the endpoint
        query = {"owner": f"SOLANA:{wallet}", "size": 100, "continuation": session}
        # Makes the request and parses the body response to JSON
        results = get(f"{base_url}/items/byOwner", query).json()
        # Updates the accumulator/list of NFTs retrieved
        mapped = [RaribleNFT(**item) for item in results["items"]]
        nfts.extend(mapped)
        # If no continuation is available it means we have the full list
        if results.get("continuation", None) is None:
            return nfts
        else:
            session = results.get("continuation")
