from typing import Any, List, Union
import pandas
import io

from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, deps

router = APIRouter()


@router.get("/", response_model=List[Any])
def read_tasks_with_benchmarks_number(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> List[schemas.Task]:
    """
    Retrieve tasks.
    """
    tasks = crud.task.get_multi_and_count_benchmarks(db, skip=skip, limit=limit)
    return tasks


@router.post("/", response_model=schemas.Task)
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    task_in: schemas.TaskCreate,
    # current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Create new task.
    """
    task = crud.task.create(db=db, obj_in=task_in)
    return task


@router.put("/{id}", response_model=schemas.Task)
def update_task(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    task_in: schemas.TaskUpdate,
    # current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Update an task.
    """
    task = crud.task.get(db=db, id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task = crud.task.update(db=db, db_obj=task, obj_in=task_in)
    return task


@router.delete("/{id}", response_model=schemas.Task)
def delete_task(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Delete an task.
    """
    task = crud.task.get(db=db, id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task = crud.task.remove(db=db, id=id)
    return task
