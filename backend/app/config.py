from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://fisher:fisher@db:5432/fisherapp"
    secret_key: str = "dev-secret-key-change-in-production"
    jwt_expiry_hours: int = 24
    cors_origins: str = "http://localhost:5173"

    blim_lucky_guess: float = 0.1
    blim_careless_error: float = 0.05
    blim_mastery_threshold: float = 0.85
    blim_entropy_termination: float = 0.15

    review_grace_days: int = 7
    review_decay_rate: float = 0.02

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
