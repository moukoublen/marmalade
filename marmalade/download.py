import requests
import shutil
import os
import re
import tempfile


def get_filename_from_header(url: str) -> str:
    headers = requests.head(url, allow_redirects=True).headers
    cd = headers.get('content-disposition')
    if not(cd):
        return ""
    filename = re.findall('filename=(.+)', cd)
    if len(filename) == 0:
        return ""
    return filename[0]


def get_file_name(url: str) -> str:
    filename = get_filename_from_header(url)
    if(filename == ""):
        filename = url.split('/').pop()
    return filename


def get_download_dir():
    tmp = os.path.join(tempfile.gettempdir(), "marmalade_downloads")
    if not(os.path.exists(tmp)):
        os.makedirs(tmp)
    return tmp


def get_file(url: str) -> str:
    download_dir = get_download_dir()
    filename = get_file_name(url)
    resp = requests.get(url, allow_redirects=True, stream=True)
    full_path_file = os.path.join(download_dir, filename)
    with open(full_path_file, 'wb') as file:
        shutil.copyfileobj(resp.raw, file)
    return full_path_file


def github_download_link(repo: str, postfix_file: str) -> str:
    return "https://github.com/{}/releases/download/{}".format(repo,
                                                               postfix_file)
