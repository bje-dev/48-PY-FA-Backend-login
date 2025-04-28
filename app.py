from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes.user import user

tags_metadata = [
    {"name": "users", "description": "Operaciones relacionadas con usuarios."}
]
app = FastAPI(
    title="API-LOGIN Infranet",
    description="Api para el login del sistema infranet",
    version="1.0.0",
    openapi_tags=tags_metadata
)
app.include_router(user)

# Configuración de CORS
origins = [
    "http://localhost",        # Dirección del frontend
    "http://localhost:3000",  # Si usas un frontend React/Vue/Angular en otro puerto
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Métodos permitidos: GET, POST, etc.
    allow_headers=["*"],  # Headers permitidos
)