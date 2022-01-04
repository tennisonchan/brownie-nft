from brownie import network
from scripts.helpers import get_account, is_development, get_contract
from scripts.advanced_collectible.deploy import deploy_collectible
from scripts.advanced_collectible.create_collectible import create_collectible
import pytest
import time


def test_can_create_collectible_integration():
    print(f"network: {network.show_active()}")

    if is_development(network.show_active()):
        pytest.skip("Only for integration testing")

    contract = deploy_collectible(forced=True)
    assert contract.tokenIds() == 0
    tx = create_collectible()
    time.sleep(60)
    assert contract.tokenIds() == 1
