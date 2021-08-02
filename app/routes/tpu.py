from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Tpu])
def read_tpus(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    q: str = None,
) -> Any:
    """
    Retrieve tpus.
    """
    tpus = crud.tpu.get_multi(db, skip=skip, limit=limit, q=q)

    return tpus


@ router.post("/", response_model=schemas.Tpu)
def create_tpu(
    *,
    db: Session = Depends(deps.get_db),
    tpu_in: schemas.TpuCreate,
    current_user: models.User = Depends(deps.GetCurrentUser('reviewer')),
) -> Any:
    """
    Create new tpu.
    """
    tpu = crud.tpu.create(db=db, obj_in=tpu_in)
    return tpu


@ router.put("/{id}", response_model=schemas.Tpu)
def update_tpu(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    tpu_in: schemas.TpuUpdate,
    current_user: models.User = Depends(deps.GetCurrentUser('reviewer')),
) -> Any:
    """
    Update an tpu.
    """
    tpu = crud.tpu.get(db=db, id=id)
    if not tpu:
        raise HTTPException(status_code=404, detail="Tpu not found")
    tpu = crud.tpu.update(db=db, db_obj=tpu, obj_in=tpu_in)
    return tpu


@ router.get("/{id}", response_model=schemas.Tpu)
def read_tpu(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Get tpu by ID.
    """
    tpu = crud.tpu.get(db=db, id=id)
    if not tpu:
        raise HTTPException(status_code=404, detail="Tpu not found")
    if not crud.user.is_superuser(current_user) and (tpu.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return tpu


@ router.delete("/{id}", response_model=schemas.Tpu)
def delete_tpu(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('reviewer')),
) -> Any:
    """
    Delete an tpu.
    """
    tpu = crud.tpu.get(db=db, id=id)
    if not tpu:
        raise HTTPException(status_code=404, detail="Tpu not found")
    tpu = crud.tpu.remove(db=db, id=id)
    return tpu
