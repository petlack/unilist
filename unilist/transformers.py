from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from unilist.utils import get_ext


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


def identify_transformer(uri, config):
    ext, compress = get_ext(uri)
    if ext == 'jsonl':
        return JsonlTransformer(config.get('jsonl', {})), compress
    return PlaintextTransformer(config.get('txt', {})), compress
