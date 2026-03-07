import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth, dashboard, placement, lessons, practice, review, settings as settings_router
from app.routers import ai_chat

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)

app = FastAPI(title="Fisher App API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(placement.router)
app.include_router(lessons.router)
app.include_router(practice.router)
app.include_router(review.router)
app.include_router(settings_router.router)
app.include_router(ai_chat.router)


@app.get("/health")
def health():
    return {"status": "ok"}
