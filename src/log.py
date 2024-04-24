import logging
import logging.handlers
from pathlib import Path

import coloredlogs  # type: ignore[reportMissingTypeStubs]

# setup logging format
format_string = "%(asctime)s | %(module)s | %(levelname)s | %(message)s"
formatter = logging.Formatter(format_string)

# set stdout logger to INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

# setup logging file
log_file = Path("src/logs/log.log")
log_file.parent.mkdir(exist_ok=True)

# setup logger file handler
# starts a new log file each day at midnight, UTC
# keeps no more than 10 days worth of logs.
file_handler = logging.handlers.TimedRotatingFileHandler(
    log_file,
    "midnight",
    utc=True,
    backupCount=10,
    encoding="utf-8",
)

file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

coloredlogs.DEFAULT_LEVEL_STYLES = {
    "info": {"color": coloredlogs.DEFAULT_LEVEL_STYLES["info"]},
    "critical": {"color": 9},
    "warning": {"color": 11},
}

# Apply coloredlogs to the stdout handler
coloredlogs.install(  # type: ignore[unknownMemberTypes]
    level=logging.INFO,
    logger=logger,
    stream=stdout_handler.stream,
)

# silence disnake's annoying info logger
logging.getLogger("disnake").setLevel(logging.WARNING)

logger = logging.getLogger()
logger.info("Logging has been initialized")


def get_logger(name: str) -> logging.Logger:
    """Return a logger."""
    return logging.getLogger(name)
