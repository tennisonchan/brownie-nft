from brownie import AdvancedCollectible, network, config
from scripts.helpers import (
    get_account,
    get_contract,
)


def deploy_collectible():
    # vrfCoordinator: 0xb3dCcb4Cf7a26f6cf6B120Cf5A73875B7BBc655B
    # linkToken: 0x01BE23585060835E02B77ef475b0Cc51aA1e0709
    # keyHash: 0x2ed0feb3e7fd2022120aa84fab1945545a9f2ffc9076fd6156fa96eaff4c1311
    # fee 0.1 LINK
    # https://docs.chain.link/docs/vrf-contracts/#rinkeby
    print("Deploying...")
    contract = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["fee"],
        {"from": get_account()},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed!")
    return contract


def main():
    print(f"Run on network: {network.show_active()}")
    deploy_collectible()
