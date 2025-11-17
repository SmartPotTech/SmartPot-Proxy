import os

# --- Configuración APP ---
API_URL = os.getenv("API_URL")
APP_TITLE = os.getenv("APP_TITLE", "SmartPot API Proxy")

# --- Configuración CORS ---
_cors_origins_str = os.getenv("CORS_ALLOWED_ORIGINS", "https://localhost:8091")
CORS_ORIGINS_LIST = [origin.strip() for origin in _cors_origins_str.split(",")]
_credentials_str = os.getenv("CORS_ALLOW_CREDENTIALS", "true")
CORS_ALLOW_CREDENTIALS = _credentials_str.lower() in ('true', '1')
_methods_str = os.getenv("CORS_ALLOW_METHODS", "*")
CORS_ALLOW_METHODS_LIST = [method.strip() for method in _methods_str.split(",")]
_headers_str = os.getenv("CORS_ALLOW_HEADERS", "*")
CORS_ALLOW_HEADERS_LIST = [header.strip() for header in _headers_str.split(",")]

# --- Security Configuration ---
SECURITY_SCHEME_NAME = os.getenv("SECURITY_SCHEME_NAME")

if not API_URL:
    raise ValueError("La variable de entorno API_URL no está definida.")

if not SECURITY_SCHEME_NAME:
    raise ValueError("SECURITY_SCHEME_NAME no está definida")

HEADERS = {
    "User-Agent": "Python-Proxy-Client/1.1",
    "Accept": "application/json",
    "Content-Type": "application/json",
}
