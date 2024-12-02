from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    # BD Api Trigger
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # Microsoft
    CLIENT_ID: str
    CLIENT_SECRET: str 
    TENANT_ID: str
    AUTHORITY: str
    REDIRECT_URI: str
    USER_MC: str
    USER_PASSWORD_MC: str