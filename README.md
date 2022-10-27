# Unilist

📑 Load any **newline**-separated file as a **generator**.

Currently supporting files located in **local** filesystem, **HTTP(s)** endpoint, **S3** URI and **plaintext**, **CSV** and **JSONL** formats. Alternatively, you can setup your own virtual URLs.

## Install
Install and update using pip:
```console
pip install unilist
```

## Usage
```python
from unilist import Unilist

lines = list(Unilist('./file.txt')))
print(lines)

csv = list(Unilist('https://example.com/file.csv'))
print(csv)

# requires Unilist.setup({ ... })
# or /usr/local/bin/aws
records = list(Unilist('s3://example/file.jsonl.gz'))
print(records)
```

## S3 setup
### boto3
If you don't mind extra dependency (boto3), install with
```console
pip install unilist[boto3]
```
Example setup
```python
Unilist.setup({
    's3': {
      'aws_access_key': '___your_access_key___',
      'aws_secret_access_key': '___your_secret_key___',
    },
})
```
### awscli
Alternatively, you can provide a path to `aws` binary.
```python
Unilist.setup({
  's3': {
    'aws_bin': '/usr/local/bin/aws'
  }
})
```

## Integration
### pandas
```python
import pandas as pd
df = pd.DataFrame(Unilist('vfs://path/to/file.jsonl'))
```

## Configuration
```python
Unilist.setup({
    's3': {
      'cache_dir': '/tmp',
      'aws_access_key': '___your_access_key___',
      'aws_secret_access_key': '___your_secret_key___',
    },
    'virtual': {
      'vfs': '/custom/root/path',
      'c4': './local/c4',
    },
    'http': {
      'headers': {
        'accept': 'text/plain',
      },
      'encoding': 'utf-8',
    },
    'jsonl': {},
})
```

# Development

## Install from source
```console
git clone git@github.com:petlack/unilist.git
pip install -e .
pip install -e .[boto3]
```

## Run tests
```console
pipenv run pytest
```

# Meta

[CONTRIBUTING](/.github/CONTRIBUTING.md)

[LICENSE (MIT)](/LICENSE)