from fastapi.exceptions import HTTPException
from app.models.accuracy_value import AccuracyValue
import logging
from app.crud.base import CRUDBase
from app.models.paper import Paper
from app.schemas.paper import PaperCreate, PaperUpdate

from app.models import (Model, Revision, Message, TaskDataset)


class CRUDPaper(CRUDBase[Paper, PaperCreate, PaperUpdate]):
    def create(self, db, *, obj_in, current_user):
        data = obj_in
        paper = Paper(
            title=data.title,
            link=data.link,
            code_link=data.code_link,
            publication_date=data.publication_date,
            authors=data.authors,
            owner=current_user
        )
        revision = Revision(
            paper=paper
        )
        messages = [Message(body="paper submited", revision=revision)]

        for model_data in data.models:
            model = Model(
                name=model_data.name,
                training_time=model_data.training_time,
                gflops=model_data.gflops,
                epochs=model_data.epochs,
                number_of_parameters=model_data.number_of_parameters,
                multiply_adds=model_data.multiply_adds,
            )

            if isinstance(model_data.dataset, str) or isinstance(model_data.task, str):
                if isinstance(model_data.task, str):
                    messages.append(Message(body="new task requested: {}".format(
                        model_data.task), revision=revision))

                if isinstance(model_data.dataset, str):
                    messages.append(Message(body="new dataset requested: {}".format(
                        model_data.dataset), revision=revision))
            else:
                task_dataset = db.query(TaskDataset).filter(
                    TaskDataset.task_id == model_data.task,
                    TaskDataset.dataset_id == model_data.dataset).first()
                if not task_dataset:
                    db.close()
                    raise HTTPException(
                        status_code=404,
                        detail="No relation between Task: {} and Dataset: {} was found"
                        .format(
                            model_data.task, model_data.dataset))
                model.task_dataset_id = task_dataset.id

            for accuracy in model_data.accuracies:
                if isinstance(accuracy.accuracy_type, str):
                    messages.append(Message(
                        body="new accuracy type requested: {}, with value {}".format(
                            accuracy.accuracy_type, accuracy.value), revision=revision))
                else:
                    model.accuracy_values.append(AccuracyValue(
                        accuracy_type_id=accuracy.accuracy_type,
                        value=accuracy.value))

            if model_data.cpu and isinstance(model_data.cpu, str):
                messages.append(Message(body="new cpu requested: {}".format(
                    model_data.cpu), revision=revision))
            else:
                model.cpu_id = model_data.cpu

            if model_data.gpu and isinstance(model_data.gpu, str):
                messages.append(Message(body="new gpu requested: {}".format(
                    model_data.gpu), revision=revision))
            else:
                model.gpu_id = model_data.gpu

            if model_data.tpu and isinstance(model_data.tpu, str):
                messages.append(Message(body="new tpu requested: {}".format(
                    model_data.tpu), revision=revision))
            else:
                model.tpu_id = model_data.tpu

            paper.models.append(model)
        revision.messages = messages
        paper.revision = revision
        try:
            db.add(paper)
            db.commit()
            db.refresh(paper)
            return paper
        except Exception as e:
            logging.error(e)
            raise HTTPException(
                status_code=404,
                detail="Error on submit paper")


paper = CRUDPaper(Paper)
