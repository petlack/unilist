import os
from urllib.parse import urlparse
from pathlib import Path


def file_exists(path):
    return os.path.exists(path)


def ensure_parent_dir(path):
    directory = os.path.dirname(path)
    ensure_dir(directory)


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def get_ext(uri):
    path = f'{urlparse(uri).netloc}{urlparse(uri).path}'
    ext = Path(path).suffix.lstrip('.')
    if ext in ['gz']:
        return Path(path[:-(len(ext)+1)]).suffix.lstrip('.'), ext
    return ext, False
