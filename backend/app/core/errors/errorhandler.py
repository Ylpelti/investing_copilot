from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.errors.exceptions import AppError
import logging

logger = logging.getLogger(__name__)


async def app_error_handler(request: Request, exc: Exception):
    if isinstance(exc, AppError):
        logger.warning(f"{exc.__class__.__name__}: {exc.message} ({exc.status_code})")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.__class__.__name__,
                "message": exc.message,
                "status_code": exc.status_code,
            },
        )

    # fallback (should rarely happen)
    logger.error(f"Unexpected non-AppError passed to app_error_handler: {exc!r}")
    return JSONResponse(
        status_code=500,
        content={"error": "InternalServerError", "message": "Unexpected error"},
    )



async def generic_exception_handler(request: Request, exc: Exception):
    """
    Catch-all handler for unexpected exceptions — prevents ugly stack traces from leaking.
    """
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": str(exc),
            "status_code": 500,
        },
    )
