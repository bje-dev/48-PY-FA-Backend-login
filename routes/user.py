from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.engine.row import Row
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet

# Generar o cargar clave para Fernet (idealmente desde un entorno seguro)
key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

@user.get("/users")
def get_all_users():
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

@user.get("/users/{id}")
def get_user_by_id(user_id: int):
    try:
        result = conn.execute(users.select().where(users.c.id == user_id)).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")

        # Convertir el resultado a un diccionario
        user_data = dict(result._mapping) if isinstance(result, Row) else dict(result)

        return JSONResponse(content=user_data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user.put("/users/{id}")
def update_user(user_id: int, user_data: User):
    try:
        # Verificar si el usuario existe
        existing_user = conn.execute(users.select().where(users.c.id == user_id)).fetchone()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Actualizar los campos del usuario
        updated_user = {
            "name": user_data.name,
            "email": user_data.email,
            "password": f.encrypt(user_data.password.encode("utf-8")),
        }

        conn.execute(users.update().where(users.c.id == user_id).values(updated_user))
        conn.commit()

        return JSONResponse(content={"message": "User updated successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user.delete("/users/{id}")
def delete_user(user_id: int):
    try:
        # Verificar si el usuario existe
        existing_user = conn.execute(users.select().where(users.c.id == user_id)).fetchone()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Eliminar el usuario
        conn.execute(users.delete().where(users.c.id == user_id))
        conn.commit()

        return JSONResponse(content={"message": "User deleted successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user.patch("/users/{id}")
def update_user_partial(user_id: int, user_data: dict):
    try:
        # Verificar si el usuario existe
        existing_user = conn.execute(users.select().where(users.c.id == user_id)).fetchone()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Filtrar los campos válidos
        update_data = {key: value for key, value in user_data.items() if key in users.columns.keys()}
        if "password" in update_data:
            # Encriptar la contraseña si se incluye en la actualización
            update_data["password"] = f.encrypt(update_data["password"].encode("utf-8"))

        # Actualizar solo los campos especificados
        conn.execute(users.update().where(users.c.id == user_id).values(**update_data))
        conn.commit()

        # Consultar el usuario actualizado
        updated_user = conn.execute(users.select().where(users.c.id == user_id)).fetchone()

        # Preparar y devolver la respuesta
        response_data = {
            "id": updated_user.id,
            "name": updated_user.name,
            "email": updated_user.email
        }
        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))