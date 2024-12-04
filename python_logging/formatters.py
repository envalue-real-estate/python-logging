import logging
import json
from datetime import datetime

from .log_context import get_log_context


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_context = get_log_context()
        log_object = {
            '@timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'application': log_context.application,
            'environment': log_context.environment,
            'request_id': log_context.request_id,
        }

        if log_context.request_path is not None:
            log_object['request'] = {
                'method': log_context.request_method,
                'path': log_context.request_path,
                'user_agent': log_context.user_agent
            }
        if log_context.response_status_code is not None:
            log_object['response'] = {
                'status_code': log_context.response_status_code
            }
        return json.dumps(log_object)
