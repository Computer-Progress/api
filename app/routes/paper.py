from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Paper])
def read_papers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve papers.
    """
    papers = crud.paper.get_multi(db, skip=skip, limit=limit)

    return papers


@router.post("/", response_model=Any)
def create_paper(
    *,
    db: Session = Depends(deps.get_db),
    paper_in: schemas.PaperCreate,
    current_user: models.User = Depends(deps.GetCurrentUser('reviewer')),
) -> Any:
    """
    Create new paper.
    """
    paper = crud.paper.create(db=db, obj_in=paper_in)
    return paper


@router.put("/{id}", response_model=schemas.Paper)
def update_paper(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    paper_in: schemas.PaperUpdate,
    current_user: models.User = Depends(deps.GetCurrentUser('reviewer')),
) -> Any:
    """
    Update an paper.
    """
    paper = crud.paper.get(db=db, id=id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    paper = crud.paper.update(db=db, db_obj=paper, obj_in=paper_in)
    return paper


@router.get("/{id}", response_model=schemas.Paper)
def read_paper(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('default')),
) -> Any:
    """
    Get paper by ID.
    """
    paper = crud.paper.get(db=db, id=id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    if not crud.user.is_superuser(current_user) and (paper.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return paper


@router.delete("/{id}", response_model=schemas.Paper)
def delete_paper(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.GetCurrentUser('admin')),
) -> Any:
    """
    Delete an paper.
    """
    paper = crud.paper.get(db=db, id=id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    paper = crud.paper.remove(db=db, id=id)
    return paper
