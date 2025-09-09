from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    @property
    def database_url(self):
        user = f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
        database = f'{self.POSTGRES_HOST}:{self.POSTGRES_HOST}/{self.POSTGRES_DB}'
        
        return f'postgres+asyncpg://{user}@{database}'
    
    class Config:
        env_file = ".env"

settings = Settings()