import pytest

from unilist import Unilist
from unilist.errors import UnknownScheme

Unilist.setup({
    'virtual': {'roots': {'tmp': './tests/test_data'}},
})


class TestVirtual:
    """Test suite for Unilist class."""

    def test_unknown_scheme(self):
        """Test that unknown scheme raises exception."""
        path = 'xyz://colors.txt'

        with pytest.raises(UnknownScheme):
            list(Unilist(path))

    def test_valid_txt_file(self):
        fruits = ['apple', 'banana', 'pear']
        assert (list(Unilist('tmp://fruits.txt')) == fruits)

    def test_valid_compressed_jsonl_file(self):
        sizes = [
            {'width': 11, 'height': 11},
            {'width': 10, 'height': 10},
            {'width': 9, 'height': 8},
        ]
        assert (list(Unilist('tmp://sizes.jsonl.gz')) == sizes)

    def test_valid_jsonl_file(self):
        fruits = [
            {'type': 'apples', 'count': 7},
            {'type': 'pears', 'count': 4},
            {'type': 'bananas', 'count': 5},
        ]
        assert (list(Unilist('tmp://fruits.jsonl')) == fruits)
