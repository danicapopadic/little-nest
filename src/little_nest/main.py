from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from little_nest.routers.auth import router as auth_router

app = FastAPI(title="Little Nest API")
app.include_router(auth_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": [
                {
                    "type": error["type"],
                    "loc": error["loc"],
                    "msg": error["msg"],
                }
                for error in exc.errors()
            ]
        },
    )
