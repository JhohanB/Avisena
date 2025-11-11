from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.chicken_incident import incidentChickenCreate, incidentChickenUpdate, incidentChickenEstado

logger = logging.getLogger(__name__)

def create_incident(db: Session, incident_ch: incidentChickenCreate) -> Optional[bool]:
    try:
        query = text("""
            INSERT INTO incidentes_gallina (
                galpon_origen, tipo_incidente, cantidad, descripcion,fecha_hora, esta_resuelto
            ) VALUES (
                :galpon_origen, :tipo_incidente, :cantidad, :descripcion, :fecha_hora, :esta_resuelto
            )
        """)
        db.execute(query, incident_ch.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear el incidente de gallina: {e}")
        raise Exception("Error de base de datos al crear el incidente de gallina")


def get_incident_chicken_by_id(db: Session, id_incident_chicken: int):
    try:
        query = text("""SELECT id_inc_gallina, galpon_origen, tipo_incidente, cantidad, descripcion, fecha_hora, esta_resuelto, galpones.nombre                    
                    FROM incidentes_gallina
                    INNER JOIN galpones ON galpones.id_galpon = incidentes_gallina.galpon_origen
                    WHERE id_inc_gallina = :id_inc_gallina""")
        result = db.execute(query, {"id_inc_gallina": id_incident_chicken}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener incidente de gallina por id: {e}")
        raise Exception("Error de base de datos al obtener el incidente de gallina")

def get_all_chicken_incidents(db: Session):
    try:
        query = text("""SELECT id_inc_gallina, galpon_origen, tipo_incidente, cantidad, descripcion, fecha_hora, esta_resuelto, galpones.nombre
                    FROM incidentes_gallina
                    INNER JOIN galpones ON galpones.id_galpon = incidentes_gallina.galpon_origen
                    """)
        result = db.execute(query).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener los aislamientos: {e}")
        raise Exception("Error de base de datos al obtener los aislamientos")

def update_chicken_incident_by_id(db: Session, incident_chicken_id: int, chicken_incident: incidentChickenUpdate) -> Optional[bool]:
    try:
   
        chicken_incident_data = chicken_incident.model_dump(exclude_unset=True)
        if not chicken_incident_data:
            return False 
        set_clauses = ", ".join([f"{key} = :{key}" for key in chicken_incident_data.keys()])
        sentencia = text(f"""
            UPDATE incidentes_gallina 
            SET {set_clauses}
            WHERE id_inc_gallina = :id_inc_gallina
        """)

        chicken_incident_data["id_inc_gallina"] = incident_chicken_id

        result = db.execute(sentencia, chicken_incident_data)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar el incidente gallina {incident_chicken_id}: {e}")
        raise Exception("Error de base de datos al actualizar el incidente gallina")
    
