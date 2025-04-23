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
