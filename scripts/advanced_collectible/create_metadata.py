from brownie import AdvancedCollectible, network
from scripts.advanced_collectible.deploy import deploy_collectible
from scripts.helpers import get_breed
from scripts.ipfs import upload_file_to_ipfs, get_ipfs_url
from scripts.metadata.sample_metadata_template import metadata_template
from pathlib import Path


def create_metadata():
    contract = deploy_collectible()
    number_collectible = contract.tokenIds()
    print(f"There are {number_collectible} of collectible(s)")

    for token_id in range(1):
        breed_index = contract.tokenIdToBreed(token_id)
        breed_name = get_breed(breed_index)
        filename = f"./metadata/{network.show_active()}/{token_id}-{breed_name}.json"
        metadata = metadata_template
        if Path(filename).exists():
            print(f"Token id {token_id} already exists!")
        else:
            print(f"Creating metadata for {token_id}: {filename}...")
            metadata["name"] = breed_name
            metadata["description"] = f"{breed_name} from Digimon"
            filename = f"{breed_name.lower()}.gif"
            image_file_path = f"./img/{filename}"
            hash = upload_file_to_ipfs(image_file_path)["Hash"]
            image_uri = get_ipfs_url(hash, filename)
            metadata["image"] = image_uri
            metadata["attributes"] = []

            print(metadata)


def main():
    print(f"Network: {network.show_active()}")
    create_metadata()
