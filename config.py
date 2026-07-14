import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "SentinelShield@2026")

    SQLALCHEMY_DATABASE_URI = "sqlite:///sentinelshield.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False