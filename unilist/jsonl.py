import json

from unilist.transformer import Transformer


class JsonlTransformer(Transformer):
    def read(self, objs):
        for obj in objs:
            yield json.loads(obj)

    def write(self, objs):
        for obj in objs:
            yield json.dumps(obj)
