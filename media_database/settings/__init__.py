from pathlib import Path

import environ
import os

env = environ.Env(
    DEBUG=(bool, True)
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env.get_value('SECRET_KEY')
ENV_TYPE = env.get_value('ENV_TYPE')
DEBUG = env.get_value('DEBUG')

if ENV_TYPE == "production":
    from .production import *
elif ENV_TYPE == "staging":
    from .staging import *
else:
    from .development import *
