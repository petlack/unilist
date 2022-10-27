import os
import requests
import gzip
from urllib.parse import urlparse

from unilist.errors import UnknownScheme, Unsupported
from unilist.utils import file_exists, ensure_parent_dir


def download_s3_file(uri, root_path, aws_bin):
    local_file_path = f"{root_path}/{uri.lstrip('s3://')}"
    if not file_exists(local_file_path):
        os.system(f'{aws_bin} s3 cp {uri} {local_file_path} --no-progress')
    return local_file_path


def read_http_file(url, **kwargs):
    res = requests.get(url)
    if res.status_code > 200:
        return []
    for line in res.iter_lines():
        yield line.decode('utf-8')


def read_virtual_file(uri, roots={'file': '/'}, **kwargs):
    uri_parsed = urlparse(uri)
    if uri_parsed.scheme not in roots:
        raise UnknownScheme(f'Unknown scheme {uri_parsed.scheme}. Configured schemes: {list(roots.keys())}')
    root_path = roots[uri_parsed.scheme]
    local_file_path = f"{root_path}/{uri_parsed.netloc}{uri_parsed.path}"
    return read_local_file(local_file_path, **kwargs)


def read_s3_file(uri, root_path='.', aws_bin='aws', **kwargs):
    local_file_path = download_s3_file(uri, root_path, aws_bin)
    return read_local_file(local_file_path, **kwargs)


def read_local_file(path, compress=False):
    if not file_exists(path) or not os.path.isfile(path):
        return []
    open_fn = gzip.open if compress else open
    omode = 'rt' if compress else 'r'
    with open_fn(path, omode) as f:
        for line in f:
            yield line.rstrip()


def write_local_file(path, objs, append=False, buffer=10*1024, compress=False):
    total = 0
    ensure_parent_dir(path)
    open_fn = gzip.open if compress else open
    omode = 'wa' if append else 'w'
    omode = f'{omode}t' if compress else omode
    oargs = {} if compress else {'buffering': buffer}
    with open_fn(path, omode, **oargs) as f:
        for obj in objs:
            f.write(obj + '\n')
            total += len(obj.encode('utf-8')) + 1
    return total


def write_virtual_file(uri, objs, roots={'file': '/'}, **kwargs):
    uri_parsed = urlparse(uri)
    root_path = roots[uri_parsed.scheme]
    local_file_path = f"{root_path}/{uri_parsed.netloc}{uri_parsed.path}"
    return write_local_file(local_file_path, objs, **kwargs)


def write_s3_file(uri, objs, root_path='.', aws_bin='aws', **kwargs):
    local_file_path = download_s3_file(uri, root_path, aws_bin)
    total = write_local_file(local_file_path, objs, **kwargs)
    os.system(f'{aws_bin} s3 cp {local_file_path} {uri} --no-progress')
    return total


def write_http_file(*args, **kwargs):
    raise Unsupported('write operation is not supported for HTTP(S)')
