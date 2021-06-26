from typing import Any, List, Union
import pandas
import io

from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, deps

router = APIRouter()


@router.get("/home", response_model=List[Any])
def get_multi_task_datasets_sota(
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


@router.get("/", response_model=List[schemas.Task])
def read_tasks(
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


@router.get("/{task_id}/{dataset_id}", response_model=Any)
def get_models(
    *,
    db: Session = Depends(deps.get_db),
    task_id: Union[int, str],
    dataset_id: Union[int, str],
):
    task = crud.task.get_models(
        db=db, task_id=task_id, dataset_id=dataset_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/{task_id}/{dataset_id}/csv", response_model=Any)
def get_models_csv(
    *,
    db: Session = Depends(deps.get_db),
    task_id: Union[int, str],
    dataset_id: Union[int, str],
):
    models = crud.task.get_models_csv(
        db=db, task_id=task_id, dataset_id=dataset_id)
    if not models:
        raise HTTPException(status_code=404, detail="models not found")

    df = pandas.DataFrame(models)
    df = df.drop(['model_id'], axis=1)
    stream = io.StringIO()

    df.to_csv(stream, index=False)

    response = StreamingResponse(iter([stream.getvalue()]),
                                 media_type="text/csv"
                                 )

    response.headers["Content-Disposition"] = f"attachment; filename={task_id}-{dataset_id}.csv"

    return response


@router.get("/{id}", response_model=Any)
def read_task(
    *,
    db: Session = Depends(deps.get_db),
    id: Union[int, str],
    # current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Get task by ID.
    """
    task = crud.task.get_task_datasets_sota(db=db, task_id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
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
