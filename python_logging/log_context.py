import os
import uuid
from contextvars import ContextVar


class LogContext:
    def __init__(self, *, request_method: str, request_path: str):
        self._application = str(os.getenv('APPLICATION', default=None))
        self._request_id = str(uuid.uuid4())
        self._request_method: str = request_method
        self._request_path: str = request_path
        self._response_status_code: int | None = None

    def get_application(self):
        return self._application

    def get_request_id(self) -> str:
        return self._request_id

    def get_request_method(self) -> str:
        return self._request_method

    def get_request_path(self) -> str:
        return self._request_path

    def get_response_status_code(self) -> int:
        return self._response_status_code

    def set_response_status_code(self, code: int):
        self._response_status_code = code


_log_context_var: ContextVar[LogContext | None] = ContextVar("log_context", default=None)


def set_log_context(log_context: LogContext):
    _log_context_var.set(log_context)


def get_log_context() -> LogContext:
    return _log_context_var.get()
