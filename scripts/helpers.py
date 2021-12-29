from brownie import (
    accounts,
    network,
    config,
)

LOCAL_ENVIRONMENT = ["development", "ganache-local"]


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
