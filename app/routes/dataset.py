from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Dataset])
def read_datasets(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Retrieve datasets.
    """
    datasets = crud.dataset.get_multi(db, skip=skip, limit=limit)

    return datasets


@router.post("/", response_model=schemas.Dataset)
def create_dataset(
    *,
    db: Session = Depends(deps.get_db),
    dataset_in: schemas.DatasetCreate,
    # current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Create new dataset.
    """
    dataset = crud.dataset.create(db=db, obj_in=dataset_in)
    return dataset


@router.put("/{id}", response_model=schemas.Dataset)
def update_dataset(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    dataset_in: schemas.DatasetUpdate,
    # current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Update an dataset.
    """
    dataset = crud.dataset.get(db=db, id=id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    dataset = crud.dataset.update(db=db, db_obj=dataset, obj_in=dataset_in)
    return dataset


@router.get("/{id}", response_model=schemas.Dataset)
def read_dataset(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Get dataset by ID.
    """
    dataset = crud.dataset.get(db=db, id=id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if (not crud.user.is_superuser(current_user)
            and dataset.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return dataset


@router.delete("/{id}", response_model=schemas.Dataset)
def delete_dataset(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Delete an dataset.
    """
    dataset = crud.dataset.get(db=db, id=id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    dataset = crud.dataset.remove(db=db, id=id)
    return dataset
