import logging
import os
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)
log_folder = './logs'
os.makedirs(log_folder, exist_ok=True)  # 폴더가 존재하지 않으면 생성
log_file_path = os.path.join(log_folder, 'app.log')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)

rotating_handler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=1 , backupCount = 7)
rotating_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(rotating_format)

logger.addHandler(console_handler)
logger.addHandler(rotating_handler)