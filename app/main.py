import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from settings import API_URL, CLEAN_HEADERS
app = FastAPI(title="SmartPot API Proxy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://wokwi.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        # 1. Tomar el body (JSON) que envía Wokwi
        body = await request.json()

        # 2. Hacer la petición a la API real (Hostinger)
        #    usando HTTP/1.1 y el User-Agent limpio.
        response = await client.post(
            f"{API_URL}/auth/login",
            json=body,
            headers=CLEAN_HEADERS
        )

        # 3. Devolver la respuesta exacta (sea 200 o 400) a Wokwi
        #    Esto pasa el token o el error de "credenciales inválidas".
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
        # 1. Copiamos las cabeceras limpias
        headers = CLEAN_HEADERS.copy()

        # 2. Obtenemos el token que Wokwi nos está enviando
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(content={"proxy_error": "Authorization header (token) faltante"}, status_code=401)

        # 3. Lo añadimos a las cabeceras que van a la API real
        headers["Authorization"] = auth_header

        # 4. Tomamos el body (JSON) de Wokwi
        body = await request.json()

        # 5. Hacemos la petición a la API real
        response = await client.post(
            f"{API_URL}/Records/Create",
            json=body,
            headers=headers
        )

        # 6. Devolvemos la respuesta exacta a Wokwi
        return Response(content=response.content,
                        status_code=response.status_code,
                        media_type=response.headers.get("Content-Type"))

    except Exception as e:
        return JSONResponse(
            content={"proxy_error": "Error interno en el proxy", "details": str(e)},
            status_code=500
        )
