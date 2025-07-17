import yaml
from apscheduler.schedulers.blocking import BlockingScheduler
from backup import Backup
from config import OssConfig, BackupConfig
import os
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(pathname)s %(levelname)s: %(message)s'
)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yaml')

def load_backup_config():
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)
    backup_cfg = BackupConfig.from_dict(config['backup'])
    logging.info(f'backup_cfg: {backup_cfg}')
    oss_cfg = backup_cfg.oss
    oss_config = OssConfig.from_dict(oss_cfg)
    src_dirs = [src_dir.dir for src_dir in backup_cfg.src_dirs]
    cache_dir = backup_cfg.cache_dir
    cron = backup_cfg.cron
    
    return oss_config, src_dirs, cache_dir, cron

def main():
    oss_config, src_dirs, cache_dir, cron = load_backup_config()
    backup = Backup(src_dirs, cache_dir, oss_config)
    scheduler = BlockingScheduler()
    # 解析 cron 表达式
    cron_fields = cron.split()
    if len(cron_fields) == 5:
        minute = cron_fields[0]
        hour = cron_fields[1]
        day = cron_fields[2]
        month = cron_fields[3]
        day_of_week = cron_fields[4]
        logging.info(f'cron: {minute} {hour} {day} {month} {day_of_week}')
        scheduler.add_job(backup.backup, 'cron',
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_of_week=day_of_week,
        )
    else:
        raise ValueError('cron 表达式格式错误')
    logging.info('定时任务启动中...')
    scheduler.start()

if __name__ == '__main__':
    main()
