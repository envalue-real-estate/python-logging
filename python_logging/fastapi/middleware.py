import logging
from datetime import datetime

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from ..log_context import set_log_context, LogContext, get_log_context


class RequestContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, *args, **kwargs) -> None:
        self.logger = logging.getLogger(__name__)
        super().__init__(*args, **kwargs)

    async def dispatch(self, request: Request, call_next):
        start = datetime.now()
        set_log_context(LogContext(request_method=request.method,
                                   request_path=request.url.path,
                                   user_agent=request.headers.get('User-Agent'),
                                   client_ip=request.client.host))
        self.logger.info(f"Startup {request.method} {request.url.path}")

        response = await call_next(request)

        # Log the processing_time (request duration) in ms
        get_log_context().processing_time = round((datetime.now() - start).total_seconds() * 1000)
        get_log_context().response_status_code = response.status_code
        self.logger.info(f"Shutdown {request.method} {request.url.path}")

        return response
