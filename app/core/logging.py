import logging
import sys
from app.core.config import settings


def setup_logging() -> logging.Logger:
    """Configures structured standard logging for CareerConnect AI."""
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers = [console_handler]

    logging.getLogger("uvicorn.access").handlers = [console_handler]
    logging.getLogger("neo4j").setLevel(logging.WARNING)
    logging.getLogger("pymongo").setLevel(logging.WARNING)

    return logging.getLogger("careerconnect")


logger = setup_logging()