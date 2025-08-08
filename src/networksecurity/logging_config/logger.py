import os
import logging


from logging.handlers import RotatingFileHandler


def setup_logging():

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    file_formatter = logging.Formatter(
        "%(asctime)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(file_formatter)
    file_handler = RotatingFileHandler(
        "logs/application.log", maxBytes=10485760, backupCount=5
    )

    file_handler.setFormatter(file_formatter)
    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])


def get_logger(name):
    """
    Get a logger for a specific module.

    Args:
        name (str): Name of the logger

    Returns:
        logging.Logger: Configured logger
    """
    setup_logging()
    return logging.getLogger(name)


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.warning("Logging Has Started")
