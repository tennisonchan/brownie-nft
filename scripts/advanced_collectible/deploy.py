from brownie import AdvancedCollectible, network, config
from scripts.helpers import (
    get_account,
    OPEN_SEA_TEST_NET_URL,
    get_contract,
    fund_contract,
)

agumon_token_uri = "https://ipfs.io/ipfs/bafkreifgmuhcggw7c5rtn2q4ro5jyxo67rw5oktabku26j6hkslcvr76uy?filename=augmon.json/"


def deploy_collectible():
    if len(AdvancedCollectible) == 0:
        # vrfCoordinator: 0xb3dCcb4Cf7a26f6cf6B120Cf5A73875B7BBc655B
        # linkToken: 0x01BE23585060835E02B77ef475b0Cc51aA1e0709
        # keyHash: 0x2ed0feb3e7fd2022120aa84fab1945545a9f2ffc9076fd6156fa96eaff4c1311
        # fee 0.1 LINK
        # https://docs.chain.link/docs/vrf-contracts/#rinkeby
        return AdvancedCollectible.deploy(
            get_contract("vrf_coordinator"),
            get_contract("link_token"),
            config["networks"][network.show_active()]["key_hash"],
            config["networks"][network.show_active()]["fee"],
            {"from": get_account()},
        )
    return AdvancedCollectible[-1]


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
