from abc import ABC, abstractmethod
from dataclasses import dataclass

import json


@dataclass
class Transformer(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def read(self, objs):
        yield from objs

    @abstractmethod
    def write(self, objs):
        yield from objs


class JsonlTransformer(Transformer):
    def read(self, objs):
        for obj in objs:
            yield json.loads(obj)

    def write(self, objs):
        for obj in objs:
            yield json.dumps(obj)


class PlaintextTransformer(Transformer):
    def read(self, objs):
        for obj in objs:
            yield obj.strip()

    def write(self, objs):
        for obj in objs:
            yield str(obj)
