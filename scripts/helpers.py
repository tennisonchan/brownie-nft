from brownie import accounts, network, config, VRFCoordinatorMock, LinkToken, Contract

LOCAL_ENVIRONMENT = ["development", "ganache-local"]

OPEN_SEA_TEST_NET_URL = "https://testnets.opensea.io/asset/{}/{}"


def is_development(active_network):
    return active_network in LOCAL_ENVIRONMENT


def is_forked_local(active_network):
    return active_network in ["mainnet-fork-dev", "mainnet-fork"]


def get_account(index=0, id=None):
    if id:
        return accounts.load(id)
    if is_development(network.show_active()) or is_forked_local(network.show_active()):
        return accounts[index]
    return accounts.add(config["wallets"]["from_key"])


mock_contracts = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def deploy_mocks():
    account = get_account()
    link_token_contract = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token_contract.address, {"from": account})
    print("LinkToken, VRFCoordinatorMock deployed!")


def get_contract(type):
    contract_type = mock_contracts[type]
    if is_development(network.show_active()):
        if len(contract_type) == 0:
            deploy_mocks()
        return contract_type[-1]

    contract_address = config["networks"][network.show_active()][type]
    return Contract.from_abi(contract_type._name, contract_address, contract_type.abi)


def fund_contract(contract_address, account=None, link_token=None, amount=None):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    amount = amount if amount else config["networks"][network.show_active()]["fee"]
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print(f"contract {contract_address} is funded!")

    return tx


BREED_MAP = {
    0: "Agumon",
    1: "Armadillomon",
    2: "Chibomon",
    3: "DemiVeeimon",
    4: "Gomamon",
    5: "Hawkmon",
    6: "Leafmon",
    7: "Minomon",
    8: "Palmon",
    9: "Patamon",
    10: "Poromon",
    11: "Tokomon",
    12: "Upamon",
    13: "Veemon",
    14: "Wormmon",
}


def get_breed(breed_index):
    return BREED_MAP[breed_index]
