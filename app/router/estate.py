from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from core.database import get_db
from app.schemas.estate import EstateCreate, EstateOut, EstateUpdate
from app.schemas.users import UserOut
from app.crud import estate as crud_estates

router = APIRouter()
modulo = 3

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def create_estate(
    finca: EstateCreate, 
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        # El rol de quien usa el endpoint
        id_rol = user_token.id_rol

        if not verify_permissions(db, id_rol, modulo, 'insertar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
        
        crud_estates.create_estate(db, finca)
        return {"message": "finca creada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by-nombre", response_model=EstateOut)
def get_estate(
    nombre: str,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        # El rol de quien usa el endpoint
        id_rol = user_token.id_rol

        if not verify_permissions(db, id_rol, modulo, 'seleccionar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")

        finca = crud_estates.get_estate_by_name(db, nombre)
        if not finca:
            raise HTTPException(status_code=404, detail="finca no encontrada")
        return finca
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/all-estates", response_model=List[EstateOut])
def get_estates(
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        # El rol de quien usa el endpoint
        id_rol = user_token.id_rol

        if not verify_permissions(db, id_rol, modulo, 'seleccionar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")

        finca = crud_estates.get_all_estate(db)
        if not finca:
            raise HTTPException(status_code=404, detail="finca no encontrada")
        return finca
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/by-id/{estate_id}")
def update_estate(
    estate_id: int, 
    finca: EstateUpdate, 
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        success = crud_estates.update_estate_by_id(db, estate_id, finca)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la finca")
        return {"message": "finca actualizada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
