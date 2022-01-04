from brownie import SimpleCollectible, network
from scripts.helpers import get_account, get_open_sea_url

agumon_token_uri = "https://ipfs.io/ipfs/bafkreifgmuhcggw7c5rtn2q4ro5jyxo67rw5oktabku26j6hkslcvr76uy?filename=augmon.json/"


def deploy_collectible():
    if len(SimpleCollectible) == 0:
        return SimpleCollectible.deploy({"from": get_account()})
    return SimpleCollectible[-1]


def create_collectible():
    account = get_account()

    contract = deploy_collectible()
    tx = contract.createCollectible(agumon_token_uri, {"from": account})
    tx.wait(1)
    print(f"View your NFT at {get_open_sea_url(contract.address, 1)}")
    return tx


def main():
    print(f"Run on network: {network.show_active()}")
    create_collectible()
