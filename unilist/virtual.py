from urllib.parse import urlparse

import unilist.readwrite as rw
from unilist.errors import UnknownScheme
from unilist.resolver import Resolver


class VirtualResolver(Resolver):
    def read(self):
        kwargs = self._read_args()

        uri_parsed = urlparse(self.uri)
        roots = kwargs.get('roots', {})

        if uri_parsed.scheme not in roots:
            raise UnknownScheme(
                f'Unknown scheme {uri_parsed.scheme}. Configured schemes: {list(roots.keys())}'
            )
        
        root_path = roots[uri_parsed.scheme]
        local_file_path = f"{root_path}/{uri_parsed.netloc}{uri_parsed.path}"
        
        return rw.read_local_file(local_file_path, **kwargs)

    def write(self, objs, **kwargs):
        write_args = self._write_args(kwargs)

        uri_parsed = urlparse(self.uri)
        roots = write_args.get('roots', {})

        root_path = roots[uri_parsed.scheme]
        local_file_path = f"{root_path}/{uri_parsed.netloc}{uri_parsed.path}"

        return rw.write_local_file(local_file_path, objs, **write_args)
