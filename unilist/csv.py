from unilist.transformer import Transformer


class CsvTransformer(Transformer):
    def __init__(self, *args):
        print(args)
        super().__init__(*args)
        self.header = self.config.get('header')
        self.delim = self.config.get('delim')
        self.columns = []

    def read(self, lines):
        if self.header:
            self.columns = next(lines, '').split(self.delim)
        for line in lines:
            yield {
                col: line.split(self.delim)[idx]
                for idx, col in enumerate(self.columns)
            }

    def write(self, objs):
        for obj in objs:
            yield self.delim.join([str(objs[col]) for col in self.columns])
