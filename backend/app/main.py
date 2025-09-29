from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from .api import auth, evaluations, essays, milestones, suggestions
from .core.config import get_settings


settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/version")
async def version() -> dict[str, str]:
    return {"app": settings.app_name, "model": settings.openai_model}


def register_routes(application: FastAPI) -> None:
    application.include_router(auth.router, prefix="/api")
    application.include_router(evaluations.router, prefix="/api")
    application.include_router(essays.router, prefix="/api")
    application.include_router(suggestions.router, prefix="/api")
    application.include_router(milestones.router, prefix="/api")


register_routes(app)


def _get_frontend_build_dir() -> Path:
    if settings.frontend_build_dir:
        return Path(settings.frontend_build_dir).expanduser().resolve()
    backend_dir = Path(__file__).resolve().parent.parent
    return (backend_dir.parent / "frontend" / "dist").resolve()


frontend_dir = _get_frontend_build_dir()

if frontend_dir.exists():
    assets_dir = frontend_dir / "assets"
    if assets_dir.exists():
        app.mount("/app/assets", StaticFiles(directory=assets_dir), name="app-assets")

    @app.get("/", include_in_schema=False)
    async def redirect_to_web_app() -> RedirectResponse:
        return RedirectResponse(url="/app", status_code=307)

    @app.get("/app", include_in_schema=False)
    async def serve_root_app() -> FileResponse:
        index_file = frontend_dir / "index.html"
        if not index_file.exists():
            raise HTTPException(status_code=404, detail="Frontend build not found")
        return FileResponse(index_file)

    @app.get("/app/{path:path}", include_in_schema=False)
    async def serve_spa_routes(path: str) -> FileResponse:
        requested = frontend_dir / path
        if requested.exists() and requested.is_file():
            return FileResponse(requested)
        index_file = frontend_dir / "index.html"
        if not index_file.exists():
            raise HTTPException(status_code=404, detail="Frontend build not found")
        return FileResponse(index_file)
