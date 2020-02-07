import logging
import sys

logging.basicConfig(
	level=logging.DEBUG,
	stream=sys.stdout,
	format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
	datefmt='%H:%M:%S',
)

def get_logger(name: str) -> logging.Logger:
	return logging.getLogger(name)
