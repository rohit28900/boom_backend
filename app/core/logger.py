from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}")

# Optional: log to file
logger.add("logs/app.log", rotation="10 MB", retention="10 days", level="INFO", format="{time} | {level} | {message}")

def get_logger():
    return logger
