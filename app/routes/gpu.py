from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Gpu])
def read_gpus(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    q: str = None,
) -> Any:
    """
    Retrieve gpus.
    """
    gpus = crud.gpu.get_multi(db, skip=skip, limit=limit, q=q)

    return gpus


@router.post("/", response_model=schemas.Gpu)
def create_gpu(
    *,
    db: Session = Depends(deps.get_db),
    gpu_in: schemas.GpuCreate,
    current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Create new gpu.
    """
    gpu = crud.gpu.create(db=db, obj_in=gpu_in)
    return gpu


@router.put("/{id}", response_model=schemas.Gpu)
def update_gpu(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    gpu_in: schemas.GpuUpdate,
    current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Update an gpu.
    """
    gpu = crud.gpu.get(db=db, id=id)
    if not gpu:
        raise HTTPException(status_code=404, detail="Gpu not found")
    gpu = crud.gpu.update(db=db, db_obj=gpu, obj_in=gpu_in)
    return gpu


@router.get("/{id}", response_model=schemas.Gpu)
def read_gpu(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Get gpu by ID.
    """
    gpu = crud.gpu.get(db=db, id=id)
    if not gpu:
        raise HTTPException(status_code=404, detail="Gpu not found")
    if not crud.user.is_superuser(current_user) and (gpu.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return gpu


@router.delete("/{id}", response_model=schemas.Gpu)
def delete_gpu(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Delete an gpu.
    """
    gpu = crud.gpu.get(db=db, id=id)
    if not gpu:
        raise HTTPException(status_code=404, detail="Gpu not found")
    gpu = crud.gpu.remove(db=db, id=id)
    return gpu
