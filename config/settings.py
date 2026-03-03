import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/ginja_ai_claims"
)

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
DEBUG = os.getenv("DEBUG", "True") == "True"
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

BENEFIT_LIMIT = 40000.00
FRAUD_THRESHOLD = 2.0

PAGE_SIZE = 10

PROJECT_NAME = "Ginja AI Claims Intelligence Platform"
PROJECT_VERSION = "1.0.0"
PROJECT_DESCRIPTION = "Backend service for health claims validation and fraud detection"
