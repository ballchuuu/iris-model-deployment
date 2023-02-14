from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    ###
    # Logging
    ##
    log_level: str = "INFO"

    ###
    # Model Details
    ###
    pickle_model_name = "log_reg_1"
    bento_server = "http://localhost:3000/classify"


settings = Settings()
