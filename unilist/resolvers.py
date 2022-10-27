from abc import ABC, abstractmethod
from dataclasses import dataclass
from urllib.parse import urlparse

import unilist.readwrite as rw
from unilist.utils import file_exists


@dataclass
class Resolver(ABC):
    def __init__(self, uri, config):
        self.uri = uri
        self.config = config
        self.compress = False

    @abstractmethod
    def read(self):
        yield from []

    @abstractmethod
    def write(self, objs):
        return 0

    def _read_args(self, kwargs={}):
        return {
            **self.config,
            **kwargs,
            'compress': self.compress,
        }

    def _write_args(self, kwargs={}):
        return {
            **self.config,
            **kwargs,
            'compress': self.compress,
        }


class HTTPResolver(Resolver):
    def read(self):
        kwargs = self._read_args()
        return rw.read_http_file(self.uri, **kwargs)

    def write(self, objs, **kwargs):
        kwargs = self._write_args(kwargs)
        return rw.write_http_file(self.uri, objs, **kwargs)


class S3Resolver(Resolver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        import boto3
        self.aws_bin = self.config.get('aws_bin')
        self.aws_access_key = self.config.get('aws_access_key')
        self.aws_secret_access_key = self.config.get('aws_secret_access_key')
        self.s3 = boto3.resource(
            's3',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    def read(self):
        kwargs = self._read_args()
        rel_file_path = self.uri[len('s3://'):]
        local_file_path = f"{self.config['cache_dir']}/{rel_file_path}"
        print(self)
        if not file_exists(local_file_path):
            if self.aws_access_key and self.aws_secret_access_key:
                rw.download_s3_boto3(
                    self.uri,
                    local_file_path,
                    s3=self.s3,
                )
            else:
                rw.download_s3_cmd(
                    self.uri,
                    local_file_path,
                    aws_bin=self.aws_bin,
                )
        return rw.read_local_file(local_file_path, **kwargs)

    def write(self, objs, **kwargs):
        kwargs = self._write_args(kwargs)
        return rw.write_s3_file(self.uri, objs, **kwargs)


class VirtualResolver(Resolver):
    def read(self):
        kwargs = self._read_args()
        return rw.read_virtual_file(self.uri, **kwargs)

    def write(self, objs, **kwargs):
        kwargs = self._write_args(kwargs)
        return rw.write_virtual_file(self.uri, objs, **kwargs)


class LocalResolver(Resolver):
    def read(self):
        kwargs = self._read_args()
        return rw.read_local_file(self.uri, **kwargs)

    def write(self, objs, **kwargs):
        kwargs = self._write_args(kwargs)
        return rw.write_local_file(self.uri, objs, **kwargs)


def identify_resolver(uri, config):
    parsed_uri = urlparse(uri)
    if parsed_uri.scheme in ['http', 'https']:
        return HTTPResolver(uri, config.get('http', {}))
    if parsed_uri.scheme == 's3':
        return S3Resolver(uri, config.get('s3', {}))
    if parsed_uri.scheme:
        return VirtualResolver(uri, config.get('virtual', {}))
    return LocalResolver(uri, config.get('local', {}))
