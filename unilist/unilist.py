from urllib.parse import urlparse

from unilist.utils import get_ext

from unilist.resolvers import (
    HTTPResolver,
    S3Resolver,
    VirtualResolver,
    LocalResolver,
)

from unilist.transformers import (
    JsonlTransformer,
    PlaintextTransformer,
)

def identify_uri(uri):
    parsed_uri = urlparse(uri)
    if parsed_uri.scheme == 'http' or parsed_uri.scheme == 'https':
        return HTTPResolver(uri, Unilist._config.get('http', {}))
    if parsed_uri.scheme == 's3':
        return S3Resolver(uri, Unilist._config.get('s3', {}))
    if parsed_uri.scheme != '':
        return VirtualResolver(uri, Unilist._config.get('virtual', {}))
    return LocalResolver(uri, Unilist._config.get('local', {}))

def identify_transformer(uri):
    ext, compress = get_ext(uri)
    if ext == 'jsonl':
        return JsonlTransformer(Unilist._config.get('jsonl', {})), compress
    return PlaintextTransformer(Unilist._config.get('txt', {})), compress

class Unilist:
    _config = {}

    def __init__(self, uri):
        self.uri = uri
        self.transformer, self.compress = identify_transformer(uri)
        self.resolver = identify_uri(uri)
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