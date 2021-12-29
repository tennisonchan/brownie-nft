from pathlib import Path
import requests

IPFS_BASE_URL = "https://ipfs.io/ipfs"
IPFS_BASE_LOCAL_URL = "http://127.0.0.1:5001"


def get_ipfs_url(hash=None, filename=None):
    print(f"Getting IPFS Url for hash {hash} with filename {filename}")
    if not hash:
        raise ValueError("Hash is required!")
    url = f"{IPFS_BASE_URL}/{hash}"
    if filename:
        url += f"?filename={filename}"

    return url


def upload_file_to_ipfs(file_path):
    print(file_path)
    with Path(file_path).open("rb") as file:
        file_binary = file.read()
        # Add file to local ipfs
        # https://docs.ipfs.io/reference/http/api/#api-v0-add
        response = requests.post(
            f"{IPFS_BASE_LOCAL_URL}/api/v0/add", files={"file": file_binary}
        )
    print(f"response: {response.json()}")
    return response.json()
