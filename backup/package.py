import tarfile
import os

class Package:
    def __init__(
            self,
            src_path: str,
            save_path: str,
    ):
        self.src_path = src_path
        self.save_path = save_path

    def pack(self):
        with tarfile.open(self.save_path, "w:gz") as tar:
            tar.add(self.src_path, arcname=os.path.basename(self.src_path))
        return self.save_path
