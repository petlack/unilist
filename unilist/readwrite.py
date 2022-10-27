import os
import gzip
from urllib.parse import urlparse

from unilist.utils import file_exists, ensure_parent_dir


def download_s3_cmd(uri, local_path, aws_bin):
    os.system(f'{aws_bin} s3 cp {uri} {local_path} --no-progress')


def download_s3_boto3(uri, local_path, s3):
    parsed_uri = urlparse(uri)
    bucket = parsed_uri.netloc
    key = parsed_uri.path.lstrip('/')
    try:
        ensure_parent_dir(local_path)
        s3.Object(bucket, key).download_file(local_path)
    except Exception as error:
        print(error)


def read_local_file(path, compress=False, **_):
    if not file_exists(path) or not os.path.isfile(path):
        return []
    open_fn = gzip.open if compress else open
    omode = 'rt' if compress else 'r'
    with open_fn(path, omode) as f:
        for line in f:
            yield line.rstrip()


def write_local_file(path, objs, append=False, buffer=10*1024, compress=False, **_):
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


def write_s3_file(uri, objs, root_path='.', aws_bin='aws', **kwargs):
    local_file_path = download_s3_file(uri, root_path, aws_bin)
    total = write_local_file(local_file_path, objs, **kwargs)
    os.system(f'{aws_bin} s3 cp {local_file_path} {uri} --no-progress')
    return total
