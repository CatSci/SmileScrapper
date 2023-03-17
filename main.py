import sys
from smilescraper.exception import CustomException
from smilescraper.logger import logging


if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as e:
        logging.info('Logging started')
        logging.error('Error divde by 0')
        raise CustomException(error_msg= e, error_detail= sys)