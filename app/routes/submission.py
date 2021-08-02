from app.models.submission import StatusEnum
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.param_functions import Body
from sqlalchemy.orm import Session

from app import crud, models, schemas, deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Submission])
def read_submissions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Retrieve submissions.
    """
    if current_user.role.value == 'default':
        submission = crud.submission.get_multi(
            db, skip=skip, limit=limit, owner_id=current_user.id
        )

    submission = crud.submission.get_multi(db, skip=skip, limit=limit)
    return submission


@router.post("/", response_model=schemas.Submission)
def create_submission(
    *,
    db: Session = Depends(deps.get_db),
    submission_in: schemas.SubmissionData,
    current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Create new submission.
    """
    submission = crud.submission.create(
        db=db,
        obj_in=submission_in,
        current_user=current_user
    )
    return submission


@router.put("/{id}/status", response_model=schemas.Submission)
def update_status_submission(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    status: StatusEnum = Body(..., embed=True),
    current_user: models.User = Depends(deps.GetCurrentUser('reviewer')),
) -> Any:
    """
    Update an submission.
    """
    submission = crud.submission.get(db=db, id=id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    print(status, flush=True)
    submission = crud.submission.update_status(
        db=db, db_obj=submission, status=status, current_user=current_user)
    return submission


@router.put("/{id}", response_model=schemas.Submission)
def update_submission(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    submission_in: schemas.SubmissionData,
    current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Update an submission.
    """
    submission = crud.submission.get(db=db, id=id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    if current_user.role.value == 'default' and submission.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    submission = crud.submission.update(db=db, db_obj=submission, obj_in=submission_in)
    return submission


@router.get("/{id}", response_model=schemas.Submission)
def read_submission(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Get submission by ID.
    """
    submission = crud.submission.get(db=db, id=id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    if current_user.role.value == 'default' and submission.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return submission


@router.get("/{id}/messages", response_model=List[schemas.Message])
def read_submission_messages(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Get submission by ID.
    """

    submission = crud.submission.get(db=db, id=id)
    messages = crud.message.get_multi(db, skip=skip, limit=limit, submission_id=id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    if current_user.role.value == 'default' and submission.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return messages


@router.post("/{id}/messages", response_model=schemas.Message)
def create_submission_messages(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.GetCurrentUser('default')),
    message: str = Body(..., embed=True)
) -> Any:
    """
    Create messages on submission
    """

    submission = crud.submission.get(db=db, id=id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    if current_user.role.value == 'default' and submission.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    message_in = schemas.MessageCreate(
        submission_id=submission.id, body=message, author_id=current_user.id)

    message = crud.message.create(db, obj_in=message_in)

    return message


@router.delete("/{id}", response_model=schemas.Submission)
def delete_submission(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Delete an submission.
    """
    submission = crud.submission.get(db=db, id=id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    submission = crud.submission.remove(db=db, id=id)
    return submission
