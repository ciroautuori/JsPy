from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.api import user
from app.core import auth
from app.core.database import engine, Base
from app.core.middleware import HttpsRedirectFixMiddleware

# Creazione delle tabelle
Base.metadata.create_all(bind=engine)
root_path = os.getenv("ROOT_PATH", "")

# Inizializzazione FastAPI con metadata per Swagger
app = FastAPI(
    title="Portfolio Booking API",
    description="API per la gestione del proprio portfolio online.",
    version="1.0",
    contact={
        "name": "Supporto",
        "email": "support@example.com",
    },
    root_path=root_path
)

# CORS Middleware
# Configurazione CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:5174",  # Alternative port
    "http://127.0.0.1:5173",  # Alternative localhost
    "http://127.0.0.1:5174",  # Alternative port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(HttpsRedirectFixMiddleware)


# Includiamo i router delle API
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/users", tags=["Users"])

openapi_schema = app.openapi()
openapi_schema["components"]["securitySchemes"] = {
    "cookieAuth": {
        "type": "apiKey",
        "in": "cookie",
        "name": "access_token",  # Nome del cookie
    }
}
for path in openapi_schema["paths"]:
    for method in openapi_schema["paths"][path]:
        openapi_schema["paths"][path][method]["security"] = [
            {"cookieAuth": []}]


@app.get("/")
def root():
    return {"message": "Welcome to the Portolio API"}
