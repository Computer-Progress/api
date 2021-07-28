from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, deps

router = APIRouter()


@router.get("/", response_model=List[Any])
def read_accuracy_types_by_task_dataset_identifier(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    task_dataset_identifier: str = None
) -> Any:
    """
    Retrieve accuracy_types.
    """
    if task_dataset_identifier:
        accuracy_types = crud.accuracy_type.get_multi_by_task_dataset_identifier(
            db, skip=skip, limit=limit, task_dataset_identifier=task_dataset_identifier)
    else:
        accuracy_types = crud.accuracy_type.get_multi(db, skip=skip, limit=limit)

    return accuracy_types



@router.post("/", response_model=schemas.AccuracyType)
def create_accuracy_type(
    *,
    db: Session = Depends(deps.get_db),
    accuracy_type_in: schemas.AccuracyTypeCreate,
    # current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Create new accuracy_type.
    """
    accuracy_type = crud.accuracy_type.create(db=db, obj_in=accuracy_type_in)
    return accuracy_type


@router.put("/{id}", response_model=schemas.AccuracyType)
def update_accuracy_type(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    accuracy_type_in: schemas.AccuracyTypeUpdate,
    # current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Update an accuracy_type.
    """
    accuracy_type = crud.accuracy_type.get(db=db, id=id)
    if not accuracy_type:
        raise HTTPException(status_code=404, detail="AccuracyType not found")
    accuracy_type = crud.accuracy_type.update(
        db=db, db_obj=accuracy_type, obj_in=accuracy_type_in)
    return accuracy_type


@router.get("/{id}", response_model=schemas.AccuracyType)
def read_accuracy_type(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Get accuracy_type by ID.
    """
    accuracy_type = crud.accuracy_type.get(db=db, id=id)
    if not accuracy_type:
        raise HTTPException(status_code=404, detail="AccuracyType not found")
    if (not crud.user.is_superuser(current_user)
            and (accuracy_type.owner_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return accuracy_type


@router.delete("/{id}", response_model=schemas.AccuracyType)
def delete_accuracy_type(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Delete an accuracy_type.
    """
    accuracy_type = crud.accuracy_type.get(db=db, id=id)
    if not accuracy_type:
        raise HTTPException(status_code=404, detail="AccuracyType not found")
    accuracy_type = crud.accuracy_type.remove(db=db, id=id)
    return accuracy_type
