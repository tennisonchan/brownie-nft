from brownie import AdvancedCollectible, network, config
from scripts.helpers import get_account, is_development, is_forked_local, get_contract
from scripts.advanced_collectible.deploy import deploy_collectible
from scripts.advanced_collectible.create_collectible import create_collectible
import pytest


def test_can_create_collectible():
    print(f"network: {network.show_active()}")

    if not is_development(network.show_active()):
        pytest.skip()

    account = get_account()
    contract = deploy_collectible()

    assert contract.tokenIds() == 0
    tx = create_collectible()
    tx.wait(1)
    request_id = tx.events["requestCollectible"]["requestId"]
    randomness = 16
    tx_fulfillRandomness = get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, randomness, contract.address, {"from": account}
    )
    tx_fulfillRandomness.wait(1)
    # token_id = tx.events["breedAssigned"]["tokenId"]
    # breed = tx.events["breedAssigned"]["breed"]
    # print(f"token_id: {token_id}")
    # print(f"breed: {breed}")

    assert contract.tokenIds() == 1
    # assert contract.requestIdToSender(request_id) == account
    assert contract.tokenIdToBreed(0) == 1
