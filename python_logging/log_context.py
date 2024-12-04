import os
import uuid
from contextvars import ContextVar
from dataclasses import dataclass


@dataclass
class LogContext:
    request_id = str(uuid.uuid4())
    request_method: str | None = None
    request_path: str | None = None
    user_agent: str | None = None
    response_status_code: int | None = None

    @property
    def application(self) -> str:
        return os.getenv('APPLICATION', default=None)

    @property
    def environment(self) -> str:
        return os.getenv('ENVIRONMENT', default='local')


_log_context_var: ContextVar[LogContext | None] = ContextVar("log_context", default=None)


def set_log_context(log_context: LogContext):
    _log_context_var.set(log_context)


def get_log_context() -> LogContext:
    log_context = _log_context_var.get()
    if log_context is None:
        _log_context_var.set(LogContext())
        log_context = _log_context_var.get()
    return log_context
