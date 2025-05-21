import environ
import os

env = environ.Env()

BASE_DIR = environ.Path(__file__) - 2
APPS_DIR = BASE_DIR.path("apps")
STORAGE_DIR = BASE_DIR.path("storages")

def read_env():
    env.read_env(os.path.join(BASE_DIR, ".env"))
