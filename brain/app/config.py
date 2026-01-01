from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """BRAIN Mock Service Settings"""
    
    APP_NAME: str = "BRAIN Mock Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    
    # Simulate processing delay (seconds)
    MOCK_DELAY_MIN: float = 0.1
    MOCK_DELAY_MAX: float = 0.5
    
    # GPU simulation
    SIMULATE_GPU: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()
