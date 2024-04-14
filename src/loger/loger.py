import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

log_file = 'app.log'
file_handler = logging.FileHandler(log_file)

file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger().addHandler(file_handler)

