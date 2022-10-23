from unilist import Unilist

if __name__ == '__main__':
    Unilist.setup({
        's3': {
            'root_path': '.',
            'aws_bin': 'aws',
        },
        'virtual': {
            'roots': {
                'dtm': '.',
            },
        },
    })

    out = Unilist('./test.jsonl.gz').write([{'a': 1}, {'a': 2}, {'a': 3}])

    print(f'{out=}')

    content = list(Unilist('./test.jsonl.gz'))

    print(f'{content=}')