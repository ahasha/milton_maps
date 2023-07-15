import logging
import sys

import pandas as pd

LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(log_file="pipeline.log"):

    # Get root logger
    root_logger = logging.getLogger()

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Create console handler and set level to INFO
    # We will log DEBUG messages to files only.
    console_handler = logging.StreamHandler(stream=sys.stderr)
    console_handler.setLevel(logging.INFO)

    # Create a file handler for DEBUG logs
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Prevent double-logging...
    root_logger.propagate = False


def log_dataframe(
    logger: logging.Logger,
    df: pd.DataFrame,
    description: str,
    loglevel: int = logging.INFO,
):
    """
    Convenience function to include a short dataframe result and description in logs
    """

    msg = f"""{description}:
    {str(df)}"""
    logger.log(loglevel, msg)
