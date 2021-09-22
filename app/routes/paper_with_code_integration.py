from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, deps

router = APIRouter()


@router.get("/{task_dataset_identifier}", response_model=List[Any])
def get_models_metrics(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    task_dataset_identifier:  str = None,
    model_name: str = None,
    paper_title: str = None
) -> List[Any]:
    """
    Retrieve tasks.
    """
    models = crud.paper_with_code.get_multi_model_metrics_by_identifier(
        db, skip=skip, limit=limit, task_dataset_identifier=task_dataset_identifier,
        model_name=model_name, paper_title=paper_title)
    return models
