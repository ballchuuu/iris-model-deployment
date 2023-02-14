from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    ###
    # BentoML settings
    ###
    pickle_model_name = "log_reg_1"
    bento_model_name = "iris_model"


settings = Settings()
