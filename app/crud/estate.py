from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional
import logging

from app.schemas.estate import EstateCreate, EstateUpdate

logger = logging.getLogger(__name__)

def create_estate(db: Session, finca: EstateCreate) -> Optional[bool]:
    try:
        sentencia = text("""
            INSERT INTO fincas (
                nombre_finca, longitud, latitud,
                id_usuario, estado_finca
            ) VALUES (
                :nombre_finca, :longitud, :latitud,
                :id_usuario, :estado_finca
            )
        """)
        db.execute(sentencia, finca.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear finca: {e}")
        raise Exception("Error de base de datos al crear la finca")


def get_estate_by_name(db: Session, nombre_finca: str):
    try:
        query = text("""SELECT id_finca, fincas.nombre_finca, longitud, latitud, fincas.id_usuario, fincas.estado_finca, usuarios.nombre
                     FROM fincas
                     INNER JOIN usuarios ON fincas.id_usuario = usuarios.id_usuario 
                     WHERE fincas.nombre_finca = :finca_name
                """)
        result = db.execute(query, {"finca_name": nombre_finca}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener la finca por nombre: {e}")
        raise Exception("Error de base de datos al obtener la finca")


def get_all_estate(db: Session):
    try:
        query = text("""SELECT id_finca, fincas.nombre_finca, longitud, latitud, fincas.id_usuario, fincas.estado_finca, usuarios.nombre
                     FROM fincas
                     INNER JOIN usuarios ON fincas.id_usuario = usuarios.id_usuario 
                """)
        result = db.execute(query).mappings().all()
        return result
    except SQLAlchemyError as e: 
        logger.error(f"Error al obtener las fincas: {e}")
        raise Exception("Error de base de datos al obtener las finca")


def update_estate_by_id(db: Session, finca_id: int, finca: EstateUpdate) -> Optional[bool]:
    try:
        # Solo los campos enviados por el cliente
        finca_data = finca.model_dump(exclude_unset=True)
        if not finca_data:
            return False  # nada que actualizar


        # Construir dinámicamente la sentencia UPDATE
        set_clauses = ", ".join([f"{key} = :{key}" for key in finca_data.keys()])
        sentencia = text(f"""
            UPDATE fincas 
            SET {set_clauses}
            WHERE id_finca = :id_finca
        """)

        # Agregar el id_finca
        finca_data["id_finca"] = finca_id

        result = db.execute(sentencia, finca_data)
        db.commit()

        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar finca {finca_id}: {e}")
        raise Exception("Error de base de datos al actualizar la finca")


def get_estate_by_id(db: Session, id_finca: int):
    try:
        query = text("""SELECT fincas.nombre_finca, longitud, latitud, fincas.id_usuario, fincas.estado_finca
                     FROM fincas
                     INNER JOIN usuarios ON fincas.id_usuario = usuarios.id_usuario 
                     WHERE fincas.id_finca = :id_finca
                """)
        result = db.execute(query, {"id_finca": id_finca}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener finca por id: {e}")
        raise Exception("Error de base de datos al obtener la finca")