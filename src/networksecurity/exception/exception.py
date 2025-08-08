import sys
from networksecurity.logging_config import get_logger

logger = get_logger(__name__)


class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_detail: sys):
        self.error_message = error_message
        _, _, exc_tb = error_detail.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.file_name, self.lineno, str(self.error_message)
        )


if __name__ == "__main__":
    try:
        logger.info("Enter the Try Block")
        a = 1 / 0
        print("This won't be printed")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
