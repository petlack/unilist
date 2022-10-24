from unilist import Unilist

Unilist.setup({
    's3': {'root_path': './tmp'}
})


class TestHTTP:
    """Test suite for Unilist class."""

    def test_invalid_path(self):
        """Test that invalid path returns empty array."""
        assert (list(Unilist('https://raw.githubusercontent.com/petlack/unilist/tests/test_data/nonexisting.jsonl')) == [])

    def test_valid_jsonl_file(self):
        fruits = [
            {'type': 'apples', 'count': 7},
            {'type': 'pears', 'count': 4},
            {'type': 'bananas', 'count': 5},
        ]
        assert (list(Unilist('https://raw.githubusercontent.com/petlack/rollup-plugin-jsonlines/main/test/fixtures/basic-jsonl/fruits.jsonl')) == fruits)
