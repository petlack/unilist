import requests

from unilist.errors import Unsupported
from unilist.resolver import Resolver


class HTTPResolver(Resolver):
    def read(self):
        kwargs = self._read_args()
        encoding = kwargs.get('encoding')

        res = requests.get(self.uri)
        if res.status_code > 200:
            return []
        for line in res.iter_lines():
            yield line.decode(encoding)

    def write(self, objs, **kwargs):
        raise Unsupported('write operation is not supported for HTTP(S)')
