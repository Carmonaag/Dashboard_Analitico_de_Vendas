
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
PORT = int(os.getenv("PORT", 8050))
