from pydantic_settings import BaseSettings
from urllib.parse import quote
from faststream.rabbit import RabbitBroker

class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    PASS_CRYPT_SCHEMES:list
    
    SECRET_KEY: str
    JWT_ALG:str
    
    BEARER_TOKEN: str
    
    RABBITMQ_HOST:str
    RABBITMQ_PORT:int
    RABBITMQ_USER:str
    RABBITMQ_PASSWORD:str
    RABBITMQ_VHOST:str
    
    REDIS_HOST:str
    REDIS_PORT:int

    
    @property
    def database_url(self):
        user = f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
        database = f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        
        return f'postgresql+asyncpg://{user}@{database}'
    
    @property
    def rabbitmq_url(self) -> str:
        user = f"{self.RABBITMQ_USER}:{quote(self.RABBITMQ_PASSWORD)}"
        server = f"{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}"
        return(
            f"ampq://{user}@{server}"
        )
        
    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
    
    class Config:
        env_file = ".env"

settings = Settings()

broker = RabbitBroker(settings.rabbitmq_url, virtualhost=settings.RABBITMQ_VHOST)