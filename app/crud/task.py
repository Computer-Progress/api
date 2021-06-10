from app.crud.base import CRUDBase
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    pass


task = CRUDTask(Task)
