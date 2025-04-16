from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet

# Generar o cargar clave para Fernet (idealmente desde un entorno seguro)
key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

from fastapi.responses import JSONResponse
from sqlalchemy.engine.row import Row

@user.get("/users")
def get_users():
    try:
        result = conn.execute(users.select()).fetchall()

        # Convertir las filas a una lista de diccionarios de manera segura
        users_list = [dict(row._mapping) if isinstance(row, Row) else dict(row) for row in result]

        return JSONResponse(content={"users": users_list}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user.post("/users")
def create_user(user_data: User):
    try:
        # Crear el nuevo usuario
        new_user = {
            "name": user_data.name,
            "email": user_data.email,
            "password": f.encrypt(user_data.password.encode("utf-8")),
        }

        # Insertar en la base de datos
        result = conn.execute(users.insert().values(new_user))

        # Obtener el ID insertado
        inserted_id = result.inserted_primary_key[0]

        # Consultar el nuevo registro
        created_user = conn.execute(users.select().where(users.c.id == inserted_id)).fetchone()

        if not created_user:
            raise HTTPException(status_code=404, detail="User not found")

        conn.commit()

        # Preparar la respuesta como JSON estructurado
        response_data = {
            "id": created_user.id,
            "name": created_user.name,
            "email": created_user.email
        }
        return JSONResponse(content=response_data, status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
