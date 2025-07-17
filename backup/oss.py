import os
import oss2


class Oss:
    def __init__(
            self,
            endpoint: str,
            access_key_id: str,
            access_key_secret: str,
            bucket: str,
            prefix: str,
    ):
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket)
        self.prefix = prefix

    def upload(self, src_name: str, oss_file_name: str):
        oss_full_name = os.path.join(self.prefix, oss_file_name)
        self.bucket.put_object_from_file(oss_full_name, src_name)
    