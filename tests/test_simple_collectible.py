from brownie import network, SimpleCollectible
from scripts.helpers import get_account, is_development, is_forked_local
from scripts.advanced_collectible.deploy import create_collectible
import pytest


def test_can_create_simple_collectible():
    if is_forked_local(network.show_active()):
        pytest.skip()
    account = get_account()
    contract = SimpleCollectible.deploy({"from": account})
    mock_uri = "mock_uri"
    print("counter", contract.tokenIds())
    assert contract.tokenIds() == 0
    contract.createCollectible(mock_uri, {"from": account})
    assert contract.ownerOf(0) == account
    assert contract.tokenIds() == 1
