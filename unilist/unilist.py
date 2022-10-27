from urllib.parse import urlparse

from unilist.utils import get_ext

from unilist.jsonl import JsonlTransformer
from unilist.plaintext import PlaintextTransformer

from unilist.s3 import S3Resolver
from unilist.http import HTTPResolver
from unilist.virtual import VirtualResolver
from unilist.local import LocalResolver


def identify_transformer(uri, config):
    ext, compress = get_ext(uri)
    if ext == 'jsonl':
        return JsonlTransformer(config.get('jsonl', {})), compress
    return PlaintextTransformer(config.get('txt', {})), compress


def identify_resolver(uri, config):
    parsed_uri = urlparse(uri)
    if parsed_uri.scheme in ['http', 'https']:
        return HTTPResolver(uri, config.get('http', {}))
    if parsed_uri.scheme == 's3':
        return S3Resolver(uri, config.get('s3', {}))
    if parsed_uri.scheme:
        return VirtualResolver(uri, config.get('virtual', {}))
    return LocalResolver(uri, config.get('local', {}))


class Unilist:
    _config = {
        'http': {
            'encoding': 'utf-8',
        }
    }

    def __init__(self, uri):
        self.uri = uri
        self.transformer, self.compress = identify_transformer(uri, Unilist._config)
        self.resolver = identify_resolver(uri, Unilist._config)
        self.resolver.compress = self.compress

    def __iter__(self):
        yield from self.transformer.read(self.resolver.read())
#     def read(self):
#         return None

    def write(self, objs, **kwargs):
        return self.resolver.write(self.transformer.write(objs), **kwargs)

    @classmethod
    def setup(cls, config):
        cls._config = {
            **cls._config,
            **config
        }
