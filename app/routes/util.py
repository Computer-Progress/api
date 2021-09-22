from typing import Any
from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic.networks import EmailStr

from app import models, schemas
from app import deps
from app.utils.email import send_test_email

router = APIRouter()


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    background_tasks: BackgroundTasks,
    email_to: EmailStr,
    current_user: models.User = Depends(deps.GetCurrentUser('super_admin')),
) -> Any:
    """
    Test emails.
    """
    print(email_to, flush=True)
    background_tasks.add_task(send_test_email, email_to=email_to)

    return {"msg": "Test email sent"}
