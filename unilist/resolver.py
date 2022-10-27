from abc import ABC, abstractmethod
from dataclasses import dataclass


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
