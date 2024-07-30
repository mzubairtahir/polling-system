"""
This module configures the logging setup for the application.
"""

import logging
import logging.config
from pollingsystem.settings.base import DEBUG

# Logging configuration

local_handler = ["console"]
prod_handler = ["file", "json_file"]


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.log",
            "formatter": "default",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5       # Keep up to 5 backup files
        },
        "json_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.json.log",
            "formatter": "json",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5       # Keep up to 5 backup files
        }
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": local_handler + prod_handler
            # "handlers": local_handler if DEBUG else prod_handler
        }
    }
}

# Apply logging configuration
logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)
