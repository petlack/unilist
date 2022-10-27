from abc import ABC, abstractmethod
from dataclasses import dataclass


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

