from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List

@dataclass_json
@dataclass
class OssConfig:
    endpoint: str = field(default='')
    access_key_id: str = field(default='') 
    access_key_secret: str = field(default='')
    bucket: str = field(default='')
    prefix: str = field(default='')

@dataclass_json
@dataclass
class BackupSrcDir:
    dir: str = field(default='')
    pv: str = field(default='')
    storage: str = field(default='')

@dataclass_json
@dataclass
class BackupConfig:
    oss: OssConfig = field(default_factory=OssConfig)
    cron: str = field(default='')
    src_dirs: List[BackupSrcDir] = field(default_factory=list)
    cache_dir: str = field(default='')