import os

# La URL de tu API real en Hostinger
API_URL = os.getenv("API_URL", "http://localhost")

if not API_URL:
    raise ValueError("La variable de entorno API_URL no está definida.")

CLEAN_HEADERS = {
    "User-Agent": "Python-Proxy-Client/1.1",
    "Accept": "application/json",
    "Content-Type": "application/json",
}
