# api_gateway/app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8001")
USER_MANAGEMENT_SERVICE_URL = os.getenv("USER_MANAGEMENT_SERVICE_URL", "http://user_management_service:8002")