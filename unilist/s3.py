import unilist.readwrite as rw
from unilist.utils import file_exists
from unilist.resolver import Resolver


class S3Resolver(Resolver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        import boto3
        self.aws_bin = self.config.get('aws_bin')
        self.aws_access_key = self.config.get('aws_access_key')
        self.aws_secret_access_key = self.config.get('aws_secret_access_key')
        self.s3 = boto3.resource(
            's3',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    def read(self):
        kwargs = self._read_args()
        rel_file_path = self.uri[len('s3://'):]
        local_file_path = f"{self.config['cache_dir']}/{rel_file_path}"
        if not file_exists(local_file_path):
            if self.aws_access_key and self.aws_secret_access_key:
                rw.download_s3_boto3(
                    self.uri,
                    local_file_path,
                    s3=self.s3,
                )
            else:
                rw.download_s3_cmd(
                    self.uri,
                    local_file_path,
                    aws_bin=self.aws_bin,
                )
        return rw.read_local_file(local_file_path, **kwargs)

    def write(self, objs, **kwargs):
        kwargs = self._write_args(kwargs)
        return rw.write_s3_file(self.uri, objs, **kwargs)
