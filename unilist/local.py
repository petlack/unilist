import unilist.readwrite as rw
from unilist.resolver import Resolver


class LocalResolver(Resolver):
    def read(self):
        kwargs = self._read_args()
        return rw.read_local_file(self.uri, **kwargs)

    def write(self, objs, **kwargs):
        kwargs = self._write_args(kwargs)
        return rw.write_local_file(self.uri, objs, **kwargs)
