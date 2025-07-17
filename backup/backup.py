import time
import os
from typing import List
from package import Package
from oss import Oss
from config import OssConfig
import logging

class Backup:
    def __init__(
            self,
            src_dirs: List[str],
            cache_dir: str,
            oss_config: OssConfig,
    ):
        self.src_dirs = src_dirs
        self.cache_dir = cache_dir
        self.oss_config = oss_config
        self.oss = Oss(
            self.oss_config.endpoint,
            self.oss_config.access_key_id,
            self.oss_config.access_key_secret,
            self.oss_config.bucket,
            self.oss_config.prefix,
        )

    def backup(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        logging.info(f'backup start at current_time: {current_time}')
        results = []
        for index, src_dir in enumerate(self.src_dirs):
            logging.info(f'backup src_dir: {src_dir}')
            save_name = os.path.join(self.cache_dir, f"{index}.tar.gz")
            if os.path.exists(save_name):
                os.remove(save_name)
            logging.info(f'backup save_name: {save_name}')
            package = Package(src_dir, save_name)
            package.pack()
            logging.info(f'backup package: {src_dir} done')
            results.append(save_name)
        logging.info('pack done')
        for result in results:
            logging.info(f'backup upload: {result}')
            self.oss.upload(result, f"{current_time}/{os.path.basename(result)}")
            logging.info(f'backup upload done: {result}')
        logging.info('backup done')
        


        
