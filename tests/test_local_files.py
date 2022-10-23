import pytest

from unilist import Unilist
from unilist.errors import UnknownScheme

Unilist.setup({
    'virtual': {'roots': {'tmp': './tests/test_data'}},
    's3': {'root_path': './tmp'},
})


class TestUnilist:
    """Test suite for Unilist class."""

    # def test_read_virtual_file(self, unilist: Unilist):
    #     """Test curve comparison"""
    #     assert list(Unilist('tmp:')) == deepcopy(unilist)

    def test_invalid_uri(self):
        """Test that invalid URI returns empty array."""
        # with pytest.raises(ValueError):
        assert (list(Unilist('tmp:')) == [])

    def test_unknown_virtual_scheme(self):
        """Test that unknown scheme raises exception."""
        path = 'xyz://colors.txt'

        with pytest.raises(UnknownScheme):
            list(Unilist(path))

    def test_valid_local_txt_file(self):
        colors = ['red', 'blue', 'green']
        assert (list(Unilist('./tests/test_data/colors.txt')) == colors)

    def test_valid_virtual_txt_file(self):
        fruits = ['apple', 'banana', 'pear']
        assert (list(Unilist('tmp://fruits.txt')) == fruits)

    def test_valid_virtual_compressed_jsonl_file(self):
        sizes = [
            {'width': 11, 'height': 11},
            {'width': 10, 'height': 10},
            {'width': 9, 'height': 8},
        ]
        assert (list(Unilist('tmp://sizes.jsonl.gz')) == sizes)

    def test_valid_http_jsonl_file(self):
        fruits = [
            {'type': 'apples', 'count': 7},
            {'type': 'pears', 'count': 4},
            {'type': 'bananas', 'count': 5},
        ]
        assert (list(Unilist('https://raw.githubusercontent.com/petlack/rollup-plugin-jsonl-import/main/test/fixtures/basic-jsonl/fruits.jsonl')) == fruits)

    def test_valid_s3_txt_file(self):
        shapes = ['circle', 'square', 'triangle']
        assert (list(Unilist('s3://unilist-public/shapes.txt')) == shapes)
