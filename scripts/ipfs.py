from pathlib import Path
import requests
import json

IPFS_BASE_URL = "https://ipfs.io/ipfs"
IPFS_BASE_LOCAL_URL = "http://127.0.0.1:5001"
IPFS_CACHE_FILE_PATH = "./metadata/ipfs_cache.json"


def get_ipfs_cache():
    if not Path(IPFS_CACHE_FILE_PATH).exists():
        return {}

    with open(IPFS_CACHE_FILE_PATH, "r") as json_file:
        return json.load(json_file)


def set_ipfs_cache(file_path, ipfs_url):
    cache = get_ipfs_cache()
    filename = file_path.split("/")[-1]
    if not cache.get(filename, None):
        print(f"[Cache] Set cache for {filename}")
        cache.update({filename: ipfs_url})
        with open(IPFS_CACHE_FILE_PATH, "w") as file:
            json.dump(cache, file)


def get_ipfs_url_from_cache(file_path):
    cache = get_ipfs_cache()
    filename = file_path.split("/")[-1]
    cache_url = cache.get(filename, None)
    if cache_url:
        print(f"[Cache] Use cached IPFS url: {cache_url}")
    else:
        print(f"[Cache] No cache for {filename}")
    return cache_url


def get_ipfs_url(hash=None, filename=None):
    print(f"Getting IPFS Url for hash {hash} with filename {filename}")
    if not hash:
        raise ValueError("Hash is required!")
    url = f"{IPFS_BASE_URL}/{hash}"
    if filename:
        url += f"?filename={filename}"

    return url


def upload_file_to_ipfs(file_path):
    url = get_ipfs_url_from_cache(file_path)
    if url:
        return url

    with Path(file_path).open("rb") as file:
        print(f"Uploading file: {file_path} to IPFS")
        file_binary = file.read()
        filename = file_path.split("/")[-1]
        # Add file to local ipfs
        # https://docs.ipfs.io/reference/http/api/#api-v0-add
        response = requests.post(
            f"{IPFS_BASE_LOCAL_URL}/api/v0/add", files={"file": file_binary}
        )
        print(f"Response: {response.json()}")
        hash = response.json()["Hash"]
        url = get_ipfs_url(hash, filename)
        set_ipfs_cache(file_path, url)
        print(f"Uploaded to IPFS at {url}")
        return url
