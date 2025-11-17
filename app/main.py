import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .settings import API_URL, APP_TITLE, CORS_ORIGINS_LIST, CORS_ALLOW_CREDENTIALS, CORS_ALLOW_METHODS_LIST, \
    CORS_ALLOW_HEADERS_LIST, HEADERS

app = FastAPI(title=APP_TITLE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS_LIST,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS_LIST,
    allow_headers=CORS_ALLOW_HEADERS_LIST,
)

client = httpx.AsyncClient()


@app.on_event("shutdown")
async def close_client():
    await client.aclose()


@app.post("/auth/login")
async def proxy_login(request: Request):
    """
    Recibe el login JSON de Wokwi y lo reenvía a la API real.
    """
    try:
        body = await request.json()

        response = await client.post(
            f"{API_URL}/auth/login",
            json=body,
            headers=HEADERS
        )

        return Response(content=response.content,
                        status_code=response.status_code,
                        media_type=response.headers.get("Content-Type"))

    except Exception as e:
        return JSONResponse(
            content={"proxy_error": "Error interno en el proxy", "details": str(e)},
            status_code=500
        )


@app.post("/Records/Create")
async def proxy_create_record(request: Request):
    """
    Recibe el 'create record' de Wokwi, le añade el token,
    y lo reenvía a la API real.
    """
    try:
        headers = HEADERS.copy()

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(content={"proxy_error": "Authorization header faltante"}, status_code=401)

        headers["Authorization"] = auth_header

        body = await request.json()

        response = await client.post(
            f"{API_URL}/Records/Create",
            json=body,
            headers=headers
        )

        return Response(content=response.content,
                        status_code=response.status_code,
                        media_type=response.headers.get("Content-Type"))

    except Exception as e:
        return JSONResponse(
            content={"proxy_error": "Error interno en el proxy", "details": str(e)},
            status_code=500
        )
