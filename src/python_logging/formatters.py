import logging
import json

from log_context import get_log_context


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_context = get_log_context()
        log_object = {
            '@timestamp': int(record.created * 1000),  # epoch ms
            'level': record.levelname,
            'message': record.getMessage(),
            'application': log_context.get_application(),
            'request_id': log_context.get_request_id(),
        }

        if log_context.get_request_path() is not None:
            log_object['request'] = {
                'method': log_context.get_request_method(),
                'path': log_context.get_request_path()
            }
        if log_context.get_response_status_code() is not None:
            log_object['response'] = {
                'status_code': log_context.get_response_status_code()
            }
        return json.dumps(log_object)