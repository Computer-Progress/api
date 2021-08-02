from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, deps

router = APIRouter()


@router.get("/{task_dataset_identifier}", response_model=List[Any])
def get_home_info(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    task_dataset_identifier:  str = None,
) -> List[Any]:
    """
    Retrieve tasks.
    """
    models = crud.paper_with_code.get_multi_model_metrics_by_identifier(
        db, skip=skip, limit=limit, task_dataset_identifier=task_dataset_identifier)
    return models


@router.get("/{task_dataset_identifier}/{model_identifier}", response_model=Any)
def get_all_datasets_for_task(
    *,
    db: Session = Depends(deps.get_db),
    task_dataset_identifier:  str = None,
    model_identifier:  str = None,
) -> Any:
    """
    Get task by ID.
    """
    model = crud.paper_with_code.get_model_metrics_by_identifier(
        db=db, task_dataset_identifier=task_dataset_identifier,
        model_identifier=model_identifier)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model
