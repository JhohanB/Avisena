from typing import List
from app.schemas.users import UserOut
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.chicken_incident import incidentChickenBase, incidentChickenOut, incidentChickenUpdate
from app.crud import chicken_incident as crud_chicken_incident

router = APIRouter()
modulo = 5

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def create_incident(
    incident_ch: incidentChickenBase, 
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
     id_rol = user_token.id_rol
     if not verify_permissions(db, id_rol, modulo, 'insertar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
     
     crud_chicken_incident.create_incident(db, incident_ch)
     return {"message": "Incidente gallina creado correctamente"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-id", response_model=incidentChickenOut)
def get_incident_by_id(
    id: int, 
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        # El rol de quien usa el endpoint
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, 'seleccionar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")

        chicken_incident = crud_chicken_incident.get_incident_chicken_by_id(db, id)
        if not chicken_incident:
            raise HTTPException(status_code=404, detail="incidente gallina no encontrado")
        return chicken_incident
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all-chicken_incidents", response_model=List[incidentChickenOut])
def get_chicken_incidents(
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol  # El rol del usuario actual

        if not verify_permissions(db, id_rol, modulo, 'seleccionar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
        
        incident_chicken = crud_chicken_incident.get_all_chicken_incidents(db)
        if not incident_chicken:
            raise HTTPException(status_code=404, detail="incidentes de gallinas no encontrados")
        return incident_chicken

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/by-id/{chicken_incident_id}")
def update_chicken_incident(
    chicken_incident_id: int, 
    cihcken_incidente: incidentChickenUpdate, 
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        
        id_rol = user_token.id_rol

        if not verify_permissions(db, id_rol, modulo, 'actualizar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
        
        success = crud_chicken_incident.update_chicken_incident_by_id(db, chicken_incident_id, cihcken_incidente)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el incidente gallina")
        return {"message": "incidente gallina actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
