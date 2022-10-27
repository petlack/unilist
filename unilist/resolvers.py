from abc import ABC, abstractmethod
from dataclasses import dataclass

import unilist.readwrite as rw


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
    def read(self):
        kwargs = self._read_args()
        return rw.read_s3_file(self.uri, **kwargs)

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
