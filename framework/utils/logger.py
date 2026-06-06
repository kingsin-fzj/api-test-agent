"""Test logger utility"""

import sys
from loguru import logger
import os

class TestLogger:
    """Centralized logging handler"""
    _configured = False
    
    @staticmethod
    def configure(log_level="INFO", log_file="logs/test.log"):
        if TestLogger._configured:
            return
        logger.remove()
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logger.add(sys.stderr, format="<level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>", level=log_level, colorize=True)
        logger.add(log_file, format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name} - {message}", level=log_level, rotation="500 MB")
        TestLogger._configured = True
    
    @staticmethod
    def get_logger(name):
        return logger.bind(name=name)
