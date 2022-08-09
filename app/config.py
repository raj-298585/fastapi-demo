from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "ACE API"
    admin_email: str ="rkuppala@barracuda.com"
    items_per_user: int = 50

settings = Settings()
