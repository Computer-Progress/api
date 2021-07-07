import logging
from typing import Any, List
from sqlalchemy.orm.session import Session
from app.models import (Task,  Model, TaskDataset, Revision, Paper)


class CRUDTask():

    def get_multi_model_metrics_by_identifier(
        self,
        db: Session, *,
        limit: int,
        skip: int,
        task_dataset_identifier:  str,
    ) -> List[Any]:

        tasks_dataset = db.query(TaskDataset).filter(
            TaskDataset.identifier == task_dataset_identifier
        ).limit(
            limit).offset(skip).subquery('tasks_dataset')

        response = db.query(
            tasks_dataset.c.identifier.label("tasks_dataset_identifier"),
            Model.identifier.label("model_identifier"),
            Model.name.label("model_name"),
            Model.hardware_burden.label("model_hardware_burden"),
            Model.gflops.label("model_gflops"),
            Model.multiply_adds.label("model_multiply_adds"),
            Paper.identifier.label("paper_identifier"),
        ).select_from(tasks_dataset)\
            .join(TaskDataset.models)\
            .join(Model.paper)\
            .join(Paper.revision)\
            .filter(Revision.status == 'approved')\
            .all()

        res = []
        if len(response):
            for row in response:
                res.append({
                    'tasks_dataset_identifier': row.tasks_dataset_identifier,
                    'model_identifier': row.model_identifier,
                    'model_name': row.model_name,
                    'model_hardware_burden': row.model_hardware_burden,
                    'model_gflops': row.model_gflops,
                    'model_multiply_adds': row.model_multiply_adds,
                    'paper_identifier': row.paper_identifier,
                })

        return res

    def get_model_metrics_by_identifier(
        self,
        db: Session, *,
        task_dataset_identifier:  str,
        model_identifier:  str,
    ) -> List[Any]:

        tasks_dataset = db.query(TaskDataset).filter(
            TaskDataset.identifier == task_dataset_identifier
        ).subquery('tasks_dataset')

        response = db.query(
            tasks_dataset.c.identifier.label("tasks_dataset_identifier"),
            Model.identifier.label("model_identifier"),
            Model.name.label("model_name"),
            Model.hardware_burden.label("model_hardware_burden"),
            Model.gflops.label("model_gflops"),
            Model.multiply_adds.label("model_multiply_adds"),
            Model.extra_training_time.label("model_extra_training_time"),
            Paper.identifier.label("paper_identifier"),
        ).select_from(tasks_dataset)\
            .join(TaskDataset.models)\
            .join(Model.paper)\
            .join(Paper.revision)\
            .filter(Revision.status == 'approved')\
            .filter(Model.identifier == model_identifier)\
            .all()

        res = None
        if len(response):
            logging.error(response)
            res = {
                'tasks_dataset_identifier': response[0].tasks_dataset_identifier,
                'model_identifier': response[0].model_identifier,
                'model_name': response[0].model_name,
                'model_hardware_burden': response[0].model_hardware_burden,
                'model_gflops': response[0].model_gflops,
                'model_multiply_adds': response[0].model_multiply_adds,
                'model_operation_per_network_pass': response[0].model_gflops if response[0].model_gflops else response[0].model_multiply_adds,

                'model_extra_training_time': response[0].model_extra_training_time,
                'paper_identifier': response[0].paper_identifier,
            }

        return res


paper_with_code = CRUDTask()
