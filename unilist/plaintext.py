from unilist.transformer import Transformer


class PlaintextTransformer(Transformer):
    def read(self, objs):
        for obj in objs:
            yield obj.strip()

    def write(self, objs):
        for obj in objs:
            yield str(obj)
