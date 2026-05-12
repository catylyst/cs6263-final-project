"""Structured JSON logging for the Adaptive RAG project.

Every production path should use structured logs instead of bare print calls.
The router and API can use this logger to trace a request by request_id.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any # The Any type is imported from the typing module to allow for flexible type annotations in the code, particularly in the JsonFormatter class where log record fields can have various types.


class JsonFormatter(logging.Formatter): # This class defines a custom log formatter that formats log records as JSON strings. It inherits from the logging.Formatter class and overrides the format method to create a JSON payload containing relevant log information, including timestamps, log levels, module names, messages, and any additional fields such as request_id, event, strategy, and complexity_label if they are present in the log record.
    """Format log records as JSON."""

    def format(self, record: logging.LogRecord) -> str:
        """Return a JSON-formatted log line.""" 
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
        }

        extra_fields = {
            "request_id": getattr(record, "request_id", None),
            "event": getattr(record, "event", None),
            "strategy": getattr(record, "strategy", None),
            "complexity_label": getattr(record, "complexity_label", None),
        }

        for key, value in extra_fields.items():
            if value is not None:
                payload[key] = value

        return json.dumps(payload)


def configure_logging(log_level: str = "INFO") -> None:
    """Configure root logging with JSON output."""
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level.upper())

    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger."""
    return logging.getLogger(name)