from unilist.resolvers import identify_resolver
from unilist.transformers import identify_transformer


class Unilist:
    _config = {}

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
