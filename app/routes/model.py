from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Model])
def read_models(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Retrieve models.
    """
    models = crud.model.get_multi(db, skip=skip, limit=limit)

    return models


@router.post("/", response_model=schemas.Model)
def create_model(
    *,
    db: Session = Depends(deps.get_db),
    model_in: schemas.ModelCreate,
    # current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Create new model.
    """
    model = crud.model.create(db=db, obj_in=model_in)
    return model


@router.put("/{id}", response_model=schemas.Model)
def update_model(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    model_in: schemas.ModelUpdate,
    # current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Update an model.
    """
    model = crud.model.get(db=db, id=id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    model = crud.model.update(db=db, db_obj=model, obj_in=model_in)
    return model


@router.get("/{id}", response_model=schemas.Model)
def read_model(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Get model by ID.
    """
    model = crud.model.get(db=db, id=id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    if not crud.user.is_superuser(current_user) and (model.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return model


@router.delete("/{id}", response_model=schemas.Model)
def delete_model(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Delete an model.
    """
    model = crud.model.get(db=db, id=id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    model = crud.model.remove(db=db, id=id)
    return model
