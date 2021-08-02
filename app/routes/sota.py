from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, deps

router = APIRouter()


@router.get("/", response_model=List[Any])
def get_home_info(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> List[Any]:
    """
    Retrieve tasks.
    """
    tasks = crud.task.get_multi_task_datasets_sota(db, skip=skip, limit=limit)
    return tasks


@router.get("/{task_id}", response_model=Any)
def get_all_datasets_for_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: Union[int, str],
    # current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Get task by ID.
    """
    task = crud.task.get_task_datasets_sota(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
