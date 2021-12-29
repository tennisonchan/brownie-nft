from brownie import network
from scripts.advanced_collectible.deploy import deploy_collectible
from scripts.helpers import (
    get_account,
    fund_contract,
)


def create_collectible():
    account = get_account()
    contract = deploy_collectible()
    fund_contract(contract.address)
    tx = contract.createCollectible({"from": account})
    tx.wait(1)
    return tx


def main():
    print(f"Run on network: {network.show_active()}")
    create_collectible()
