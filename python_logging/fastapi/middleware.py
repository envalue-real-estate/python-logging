import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from ..log_context import set_log_context, LogContext, get_log_context


class RequestContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, *args, **kwargs) -> None:
        self.logger = logging.getLogger(__name__)
        super().__init__(*args, **kwargs)

    async def dispatch(self, request: Request, call_next):
        set_log_context(LogContext(request_method=request.method,
                                   request_path=request.url.path,
                                   user_agent=request.headers.get('User-Agent')))
        self.logger.info(f"Startup {request.url.path}")

        response = await call_next(request)

        get_log_context().response_status_code = response.status_code
        self.logger.info(f"Shutdown {request.url.path}")

        return response
