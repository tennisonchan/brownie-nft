from brownie import network
from scripts.helpers import get_account, get_breed, get_open_sea_url
from scripts.advanced_collectible.deploy import deploy_collectible
from scripts.ipfs import get_ipfs_url_from_cache


def set_token_uri(contract, token_id, token_uri):
    account = get_account()
    tx = contract.setTokenURI(token_id, token_uri, {"from": account})
    tx.wait(1)
    print(f"You can view the NFT at {get_open_sea_url(contract.address, token_id)}")


def main():
    print(f"[Network]: {network.show_active()}")
    contract = deploy_collectible()
    number_collectibles = contract.tokenIds()

    for token_id in range(number_collectibles):
        print(
            f"contract.tokenURI(token_id) at {token_id}: {contract.tokenURI(token_id)}"
        )
        if not contract.tokenURI(token_id).startswith("https://"):
            breed = get_breed(contract.tokenIdToBreed(token_id))
            filename = f"{token_id}-{breed.lower()}.json"
            token_uri = get_ipfs_url_from_cache(filename)
            set_token_uri(contract, token_id, token_uri)
