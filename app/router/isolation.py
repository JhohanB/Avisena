from typing import List
from app.schemas.users import UserOut
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.isolation import IsolationCreate, IsolationOut, IsolationUpdate
from app.crud import isolation as crud_isolation

router = APIRouter()
modulo = 5

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def create_isolation(
    isolation: IsolationCreate, 
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
     id_rol = user_token.id_rol
     if not verify_permissions(db, id_rol, modulo, 'insertar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
     
     crud_isolation.create_isolation(db, isolation)
     return {"message": "Aislamiento creado correctamente"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-id", response_model=IsolationOut)
def get_isolation(
    id: int, 
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        # El rol de quien usa el endpoint
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, 'seleccionar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")

        isolation = crud_isolation.get_isolation_by_id(db, id)
        if not isolation:
            raise HTTPException(status_code=404, detail="Aislamiento no encontrado")
        return isolation
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all-isolation", response_model=List[IsolationOut])
def get_isolations(
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol  # El rol del usuario actual

        if not verify_permissions(db, id_rol, modulo, 'seleccionar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
        
        isolations = crud_isolation.get_all_isolations(db)
        if not isolations:
            raise HTTPException(status_code=404, detail="Aislamientos no encontrados")
        return isolations

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/by-id/{isolation_id}")
def update_isolations(
    isolation_id: int, 
    isolation: IsolationUpdate, 
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol  # El rol del usuario actual

        if not verify_permissions(db, id_rol, modulo, 'actualizar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
        
        success = crud_isolation.update_isolation_by_id(db, isolation_id, isolation)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el aislamiento")
        return {"message": "Aislamiento actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
