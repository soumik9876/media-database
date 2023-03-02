from pathlib import Path

import environ
import os

env = environ.Env(
    DEBUG=(bool, True)
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

if env.str('ENV_TYPE') == 'STAGING':
    from .staging import *
elif env.str('ENV_TYPE') == 'PRODUCTION':
    from .production import *
else:
    from .development import *

