from pydantic_settings import BaseSettings
class S(BaseSettings):
 secret_key:str='change-me';admin_email:str='admin@example.com';admin_password:str='ChangeMe123!';app_language:str='uk'
s=S()
