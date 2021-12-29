from pathlib import Path
import requests
import os
from scripts.ipfs import get_ipfs_url

PINATA_BASE_URL = "https://api.pinata.cloud"
PIN_FILE_TO_IPFS_URL = "/pinning/pinFileToIPFS"

TEST_FILE_PATH = "./img/agumon.gif"

# https://docs.pinata.cloud/api-pinning/pin-file
def upload_file_to_pinata(file_path):
    with Path(file_path).open("rb") as file:
        file_binary = file.read()
        filename = file_path.split("/")[-1]
        headers = get_headers()
        url = PINATA_BASE_URL + PIN_FILE_TO_IPFS_URL
        print(f"Uploading filename {filename} to {url}")
        response = requests.post(
            url,
            files={"file": (filename, file_binary)},
            headers=headers,
        )
        # {'IpfsHash': string, 'PinSize': number, 'Timestamp': '2021-12-29T21:24:32.326Z'}
        print(response.json())
        hash = response.json()["IpfsHash"]
        url = get_ipfs_url(hash, filename)
        print(f"Uploaded with hash {hash} at {url}")
        return url


def get_headers():
    pinata_api_key = os.environ.get("PINATA_API_KEY")
    pinata_secret_api_key = os.environ.get("PINATA_SECRET_API_KEY")

    if not pinata_api_key or not pinata_secret_api_key:
        raise ValueError(
            "Missing PINATA_API_KEY or PINATA_SECRET_API_KEY to use Pinata"
        )

    return {
        "pinata_api_key": pinata_api_key,
        "pinata_secret_api_key": pinata_secret_api_key,
    }


# def main():
#     upload_file_to_pinata(TEST_FILE_PATH)
