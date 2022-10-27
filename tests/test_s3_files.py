import os
from unilist import Unilist

Unilist.setup({
    's3': {
        'cache_dir': './tmp',
        # 'aws_bin': 'aws',
        'aws_access_key': os.environ['AWS_ACCESS_KEY'],
        'aws_secret_access_key': os.environ['AWS_SECRET_ACCESS_KEY'],
    },
})


class TestS3:
    """Test suite for Unilist class."""

    def test_invalid_path(self):
        """Test that invalid path returns empty array."""
        assert (list(Unilist('s3://unilist-public/nonexisting.txt')) == [])

    def test_valid_txt_file(self):
        colors = ['red', 'blue', 'green']
        assert (list(Unilist('s3://unilist-public/colors.txt')) == colors)

    def test_valid_compressed_jsonl_file(self):
        sizes = [
            {'width': 11, 'height': 11},
            {'width': 10, 'height': 10},
            {'width': 9, 'height': 8},
        ]
        assert (list(Unilist('s3://unilist-public/sizes.jsonl.gz')) == sizes)

    def test_valid_jsonl_file(self):
        fruits = [
            {'type': 'apples', 'count': 7},
            {'type': 'pears', 'count': 4},
            {'type': 'bananas', 'count': 5},
        ]
        assert (list(Unilist('s3://unilist-public/fruits.jsonl')) == fruits)
