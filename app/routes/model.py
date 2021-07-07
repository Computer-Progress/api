from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, deps

from fastapi.responses import StreamingResponse
import pandas
import io

router = APIRouter()


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
    model_keys = ['task_name',
                  'dataset_name',
                  'model_id',
                  'paper_publication_date',
                  'paper_title',
                  'paper_link',
                  'paper_code_link',
                  'model_name']
    computing_power_keys = ['model_gflops',
                            'model_multiply_adds',
                            'model_operation_per_network_pass',
                            'model_extra_training_time',
                            'model_number_of_cpus',
                            'model_cpu',
                            'model_number_of_gpus',
                            'model_gpu',
                            'model_number_of_tpus',
                            'model_tpu',
                            'model_training_time',
                            'model_hardware_burden',
                            'model_number_of_parameters',
                            'model_epochs']
    accuracy_key = [k for k in models[0].keys()
                    if k not in model_keys and k not in computing_power_keys]
    res_keys = [*model_keys, *accuracy_key[::-1], *computing_power_keys]

    df = pandas.DataFrame(models, columns=res_keys)
    df = df.drop(['model_id'], axis=1)
    stream = io.StringIO()
    ['']

    df.to_csv(stream, index=False)

    response = StreamingResponse(iter([stream.getvalue()]),
                                 media_type="text/csv"
                                 )

    response.headers["Content-Disposition"] = f"attachment; filename={task_id}-{dataset_id}.csv"

    return response


@router.get("/", response_model=List[schemas.Model])
def read_models(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Retrieve models.
    """
    models = crud.model.get_multi(db, skip=skip, limit=limit)

    return models


@router.post("/", response_model=schemas.Model)
def create_model(
    *,
    db: Session = Depends(deps.get_db),
    model_in: schemas.ModelCreate,
    # current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Create new model.
    """
    model = crud.model.create(db=db, obj_in=model_in)
    return model


@router.put("/{id}", response_model=schemas.Model)
def update_model(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    model_in: schemas.ModelUpdate,
    # current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Update an model.
    """
    model = crud.model.get(db=db, id=id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    model = crud.model.update(db=db, db_obj=model, obj_in=model_in)
    return model


@router.get("/{id}", response_model=schemas.Model)
def read_model(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Get model by ID.
    """
    model = crud.model.get(db=db, id=id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    if not crud.user.is_superuser(current_user) and (model.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return model


@router.delete("/{id}", response_model=schemas.Model)
def delete_model(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Delete an model.
    """
    model = crud.model.get(db=db, id=id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    model = crud.model.remove(db=db, id=id)
    return model
