from brownie import AdvancedCollectible, network
from scripts.advanced_collectible.deploy import deploy_collectible
from scripts.helpers import get_breed
from scripts.pinata import upload_file_to_pinata
from scripts.ipfs import upload_file_to_ipfs, get_ipfs_url
from metadata.sample_metadata import metadata_template
from pathlib import Path
import json


def create_metadata():
    contract = deploy_collectible()
    number_collectible = contract.tokenIds()
    print(f"There are {number_collectible} of collectible(s)")

    for token_id in range(1):
        breed_index = contract.tokenIdToBreed(token_id)
        breed_name = get_breed(breed_index)
        metadata_filename = f"{token_id}-{breed_name.lower()}.json"
        metadata_file_path = f"./metadata/{network.show_active()}/{metadata_filename}"
        metadata = metadata_template
        if Path(metadata_file_path).exists():
            print(f"Token id {token_id} already exists!")
        else:
            print(f"Creating metadata for {token_id} in {metadata_file_path}...")
            metadata["name"] = breed_name
            metadata["description"] = f"{breed_name} from Digimon"
            filename = f"{breed_name.lower()}.gif"
            image_file_path = f"./img/{filename}"
            metadata["image"] = upload_file_to_pinata(image_file_path)
            # metadata["image"] = upload_file_to_ipfs(image_file_path)
            metadata["attributes"] = []
            print(metadata)

            with open(metadata_file_path, "w+") as file:
                json.dump(metadata, file)

            # ipfs_url = upload_file_to_ipfs(metadata_file_path)
            ipfs_url = upload_file_to_pinata(metadata_file_path)
            print(f"Uploaded metadata to {ipfs_url}")


def main():
    print(f"Network: {network.show_active()}")
    create_metadata()
