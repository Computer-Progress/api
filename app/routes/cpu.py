from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Cpu])
def read_cpus(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Retrieve cpus.
    """
    cpus = crud.cpu.get_multi(db, skip=skip, limit=limit)

    return cpus


@router.post("/", response_model=schemas.Cpu)
def create_cpu(
    *,
    db: Session = Depends(deps.get_db),
    cpu_in: schemas.CpuCreate,
    current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Create new cpu.
    """
    cpu = crud.cpu.create(db=db, obj_in=cpu_in)
    return cpu


@router.put("/{id}", response_model=schemas.Cpu)
def update_cpu(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    cpu_in: schemas.CpuUpdate,
    current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Update an cpu.
    """
    cpu = crud.cpu.get(db=db, id=id)
    if not cpu:
        raise HTTPException(status_code=404, detail="Cpu not found")
    cpu = crud.cpu.update(db=db, db_obj=cpu, obj_in=cpu_in)
    return cpu


@router.get("/{id}", response_model=schemas.Cpu)
def read_cpu(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Get cpu by ID.
    """
    cpu = crud.cpu.get(db=db, id=id)
    if not cpu:
        raise HTTPException(status_code=404, detail="Cpu not found")
    if not crud.user.is_superuser(current_user) and (cpu.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return cpu


@router.delete("/{id}", response_model=schemas.Cpu)
def delete_cpu(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Delete an cpu.
    """
    cpu = crud.cpu.get(db=db, id=id)
    if not cpu:
        raise HTTPException(status_code=404, detail="Cpu not found")
    cpu = crud.cpu.remove(db=db, id=id)
    return cpu
