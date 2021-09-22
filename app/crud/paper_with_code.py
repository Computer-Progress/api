import logging
from typing import Any, List
from sqlalchemy.orm.session import Session
from app.models import (Model, TaskDataset, Paper)


class CRUDTask():

    def get_multi_model_metrics_by_identifier(
        self,
        db: Session, *,
        limit: int,
        skip: int,
        task_dataset_identifier:  str,
        paper_title: str = None,
        model_name: str = None
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
            Paper.title.label("paper_title"),
            Paper.pwc_link.label("paper_pwc_link"),
            Paper.link.label("paper_link")).select_from(tasks_dataset)\
            .join(TaskDataset.models)\
            .join(Model.paper)\
            .filter(Paper.is_public)\

        if model_name:
            response = response.filter(Model.name.ilike(model_name))
        if paper_title:
            response = response.filter(Paper.title.ilike(paper_title))

        response = response.all()

        res = []
        if len(response):
            for row in response:
                res.append({
                    'tasks_dataset_identifier': row.tasks_dataset_identifier,
                    'model_identifier': row.model_identifier,
                    'model_name': row.model_name,
                    'model_hardware_burden': row.model_hardware_burden,
                    'model_operation_per_network_pass': row.model_gflops if row.model_gflops else row.model_multiply_adds,
                    'paper_identifier': row.paper_identifier,
                    'paper_title': row.paper_title,
                    'paper_pwc_link': row.paper_pwc_link,
                    'paper_link': row.paper_link,
                })

        return res


paper_with_code = CRUDTask()
