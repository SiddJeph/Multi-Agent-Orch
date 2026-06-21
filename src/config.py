from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_api_key: str = ""
    llm_model: str = "gemini-2.0-flash"
    database_url: str = "postgresql+psycopg://user:pass@localhost:5432/maco"
    log_level: str = "INFO"
    max_iterations: int = 3
    workspace_dir: str = "workspace"

    model_config = {"env_file": ".env", "env_prefix": ""}


settings = Settings()
