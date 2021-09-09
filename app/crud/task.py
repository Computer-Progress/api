import logging
from typing import Any, List, Union
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func
from app.crud.base import CRUDBase
from app.schemas.task import TaskCreate, TaskUpdate, TaskDatasetModels
from app.models import (Task, Dataset, Model, TaskDataset,
                        TaskDatasetAccuracyType, AccuracyValue,
                        AccuracyType, Paper,
                        Cpu, Tpu, Gpu)


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):

    def get_multi_and_count_benchmarks(
        self, db: Session, *, skip: int = 0, limit: int = 100, q
    ) -> List[Any]:

        if q:
            return db.query(Task.id, Task.name, Task.identifier)\
                .filter(Task.name.ilike("%{}%".format(q)))\
                .offset(skip)\
                .limit(limit).all()

        dataset_count = db.query(
            func.count(TaskDataset.id).label('number_of_benchmarks'),
            TaskDataset.task_id
        )\
            .group_by(TaskDataset.task_id).subquery('dataset_count')

        tasks = db.query(
            Task.id,
            Task.name,
            Task.image,
            Task.identifier,
            dataset_count.c.number_of_benchmarks
        )\
            .join(dataset_count, dataset_count.c.task_id == Task.id)\
            .offset(skip).limit(limit)\
            .all()

        return tasks

    def get_multi_task_datasets_sota(
            self,
            db: Session, *,
            skip: int = 0,
            limit: int = 100) -> List[TaskDatasetModels]:

        accuracy = db.query(
            func.max(AccuracyValue.value).label("value"),
            Model.task_dataset_id
        )\
            .select_from(AccuracyValue)\
            .join(AccuracyValue.model)\
            .join(TaskDatasetAccuracyType,
                  TaskDatasetAccuracyType.accuracy_type_id ==
                  AccuracyValue.accuracy_type_id
                  )\
            .join(Model.paper)\
            .filter(TaskDatasetAccuracyType.main)\
            .filter(Paper.is_public)\
            .group_by(Model.task_dataset_id)\
            .subquery('accuracy')

        bestModel = db.query(
            accuracy.c.value,
            Model.name,
            Model.id,
            Model.hardware_burden,
            Model.paper_id,
            Model.task_dataset_id).select_from(accuracy)\
            .join(Model, Model.id == (db.query(
                Model.id
            ).select_from(Model)
                .join(AccuracyValue.model)
                .join(TaskDatasetAccuracyType,
                      TaskDatasetAccuracyType.accuracy_type_id ==
                      AccuracyValue.accuracy_type_id
                      )
                .filter(TaskDatasetAccuracyType.main)
                .filter(accuracy.c.task_dataset_id == Model.task_dataset_id)
                .filter(AccuracyValue.value == accuracy.c.value)
                .limit(1)
            )
        ).subquery('best_model')

        tasks = db.query(Task).limit(5).subquery('tasks')

        response = db.query(
            tasks.c.id.label("task_id"),
            tasks.c.name.label("task_name"),
            tasks.c.identifier.label("task_identifier"),
            Dataset.id.label("dataset_id"),
            Dataset.name.label("dataset_name"),
            Dataset.identifier.label("dataset_identifier"),
            AccuracyType.name.label("accuracy_type_name"),
            bestModel.c.task_dataset_id.label("task_dataset_id"),
            bestModel.c.id.label("model_id"),
            bestModel.c.name.label("model_name"),
            bestModel.c.hardware_burden.label("model_hardware_burden"),
            bestModel.c.value.label("model_accuracy"),
            Paper.link.label("paper_url"),
            Paper.title.label("paper_title"),
            Paper.publication_date.label('paper_publication_date')

        ).select_from(tasks)\
            .join(TaskDataset, tasks.c.id == TaskDataset.task_id)\
            .join(TaskDataset.dataset)\
            .join(TaskDataset.accuracy_types)\
            .join(TaskDatasetAccuracyType.accuracy_type)\
            .join(bestModel, bestModel.c.task_dataset_id == TaskDataset.id)\
            .join(Paper, Paper.id == bestModel.c.paper_id)\
            .filter(TaskDatasetAccuracyType.main)\
            .all()

        res = []
        for row in response:
            current_item = (
                next((item for item in res if item["task_id"] == row.task_id), None))
            if current_item:
                current_item['datasets'].append({
                    'dataset_id': row.dataset_id,
                    'dataset_name': row.dataset_name,
                    'dataset_identifier': row.dataset_identifier,
                    'task_dataset_id': row.task_dataset_id,
                    'accuracy_name': row.accuracy_type_name,
                    'sota_id': row.model_id,
                    'sota_name': row.model_name,
                    'sota_accuracy_value': row.model_accuracy,
                    'sota_hardware_burden': row.model_hardware_burden,
                    'sota_paper_link': row.paper_url,
                    'sota_paper_publication_date': row.paper_publication_date,
                    'sota_paper_title': row.paper_title

                })
            else:
                new_item = {
                    'task_id': row.task_id,
                    'task_identifier': row.task_identifier,
                    'task_name': row.task_name,
                    'datasets': [{
                        'dataset_id': row.dataset_id,
                        'dataset_name': row.dataset_name,
                        'dataset_identifier': row.dataset_identifier,
                        'task_dataset_id': row.task_dataset_id,
                        'accuracy_name': row.accuracy_type_name,
                        'sota_id': row.model_id,
                        'sota_name': row.model_name,
                        'sota_accuracy_value': row.model_accuracy,
                        'sota_hardware_burden': row.model_hardware_burden,
                        'sota_paper_link': row.paper_url,
                        'sota_paper_publication_date': row.paper_publication_date,
                        'sota_paper_title': row.paper_title


                    }],
                }
                res.append(new_item)

        return res

    def get_task_datasets_sota(
        self,
        db: Session, *,
        task_id: Union[int, str],
    ) -> TaskDatasetModels:

        accuracy = db.query(
            func.max(AccuracyValue.value).label("value"),
            Model.task_dataset_id
        )\
            .select_from(AccuracyValue)\
            .join(AccuracyValue.model)\
            .join(TaskDatasetAccuracyType,
                  TaskDatasetAccuracyType.accuracy_type_id ==
                  AccuracyValue.accuracy_type_id
                  )\
            .join(Model.paper)\
            .filter(TaskDatasetAccuracyType.main)\
            .filter(Paper.is_public)\
            .group_by(Model.task_dataset_id)\
            .subquery('accuracy')

        bestModel = db.query(
            accuracy.c.value,
            Model.name,
            Model.id,
            Model.hardware_burden,
            Model.paper_id,
            Model.task_dataset_id).select_from(accuracy)\
            .join(Model, Model.id == (db.query(
                Model.id
            ).select_from(Model)
                .join(AccuracyValue.model)
                .join(TaskDatasetAccuracyType,
                      TaskDatasetAccuracyType.accuracy_type_id ==
                      AccuracyValue.accuracy_type_id
                      )
                .filter(TaskDatasetAccuracyType.main)
                .filter(accuracy.c.task_dataset_id == Model.task_dataset_id)
                .filter(AccuracyValue.value == accuracy.c.value)
                .limit(1)
            )
        ).subquery('best_model')

        filterTask = (Task.id == task_id) if isinstance(
            task_id, int) else (Task.identifier == task_id)
        tasks = db.query(Task).filter(filterTask).limit(5).subquery('tasks')

        response = db.query(
            tasks.c.id.label("task_id"),
            tasks.c.identifier.label("task_identifier"),
            tasks.c.name.label("task_name"),
            tasks.c.image.label("task_image"),
            tasks.c.description.label("task_description"),
            Dataset.id.label("dataset_id"),
            Dataset.identifier.label("dataset_identifier"),
            Dataset.name.label("dataset_name"),
            AccuracyType.name.label("accuracy_type_name"),
            bestModel.c.task_dataset_id.label("task_dataset_id"),
            bestModel.c.id.label("model_id"),
            bestModel.c.name.label("model_name"),
            bestModel.c.hardware_burden.label("model_hardware_burden"),
            bestModel.c.value.label("model_accuracy"),
            Paper.title.label("paper_title"),
            Paper.link.label("paper_url"),
            Paper.publication_date.label('paper_publication_date')
        ).select_from(tasks)\
            .join(TaskDataset, tasks.c.id == TaskDataset.task_id)\
            .join(TaskDataset.dataset)\
            .join(TaskDataset.accuracy_types)\
            .join(TaskDatasetAccuracyType.accuracy_type)\
            .join(bestModel, bestModel.c.task_dataset_id == TaskDataset.id)\
            .join(Paper, Paper.id == bestModel.c.paper_id)\
            .filter(TaskDatasetAccuracyType.main)\
            .all()

        res = None
        if len(response):
            res = {
                'task_id': response[0].task_id,
                'task_identifier': response[0].task_identifier,
                'task_name': response[0].task_name,
                'task_image': response[0].task_image,
                'task_description': response[0].task_description,
                'datasets': [],
            }
            for row in response:
                res['datasets'].append({
                    'dataset_id': row.dataset_id,
                    'dataset_name': row.dataset_name,
                    'dataset_identifier': row.dataset_identifier,
                    'task_dataset_id': row.task_dataset_id,
                    'accuracy_name': row.accuracy_type_name,
                    'sota_id': row.model_id,
                    'sota_name': row.model_name,
                    'sota_accuracy_value': row.model_accuracy,
                    'sota_hardware_burden': row.model_hardware_burden,
                    'sota_paper_link': row.paper_url,
                    'sota_paper_publication_date': row.paper_publication_date,
                    'sota_paper_title': row.paper_title,

                })

        return res

    def get_models(
        self,
        db: Session, *,
        task_id: Union[int, str],
        dataset_id: Union[int, str],
    ) -> TaskDatasetModels:

        filterTask = (Task.id == task_id) if isinstance(
            task_id, int) else (Task.identifier == task_id)
        filterDataset = (Dataset.id == dataset_id) if isinstance(
            dataset_id, int) else (Dataset.identifier == dataset_id)

        task_dataset = db.query(
            Task.id.label('task_id'),
            Task.identifier.label('task_identifier'),
            Task.name.label('task_name'),
            Task.image.label('task_image'),
            Dataset.id.label('dataset_id'),
            Dataset.identifier.label('dataset_identifier'),
            Dataset.name.label('dataset_name'),
            AccuracyType.name.label('accuracy_type_name'),
            AccuracyType.description.label('accuracy_type_description'),
            TaskDatasetAccuracyType.main.label('accuracy_type_main'),
        ).select_from(TaskDataset)\
            .join(TaskDataset.task)\
            .join(TaskDataset.dataset)\
            .join(TaskDataset.accuracy_types)\
            .join(TaskDatasetAccuracyType.accuracy_type)\
            .filter(
                filterTask,
                filterDataset,
        )\
            .all()

        task_dataset_res = {}
        if len(task_dataset):
            task_dataset_res = {
                'task_id': task_dataset[0].task_id,
                'task_name': task_dataset[0].task_name,
                'task_identifier': task_dataset[0].task_identifier,
                'task_image': task_dataset[0].task_image,
                'dataset_id': task_dataset[0].dataset_id,
                'dataset_identifier': task_dataset[0].dataset_identifier,
                'dataset_name': task_dataset[0].dataset_name,
                'accuracy_types': [
                    {
                        'name': acc.accuracy_type_name,
                        'description': acc.accuracy_type_description,
                        'main': acc.accuracy_type_main
                    } for acc in task_dataset
                ]

            }

        models = db.query(
            Model.id.label('model_id'),
            Model.name.label('model_name'),
            Model.gflops.label('model_gflops'),
            Model.number_of_parameters.label('model_number_of_parameters'),
            Model.multiply_adds.label('model_multiply_adds'),
            Model.hardware_burden.label('model_hardware_burden'),
            AccuracyValue.value.label('accuracy_value'),
            AccuracyType.name.label('accuracy_type'),
            Paper.title.label('paper_title'),
            Paper.link.label('paper_link'),
            Paper.code_link.label('paper_code_link'),
            Paper.publication_date.label('paper_publication_date'),
        ).join(TaskDataset.models)\
            .join(Model.accuracy_values)\
            .join(AccuracyValue.accuracy_type)\
            .join(Model.paper)\
            .join(TaskDataset.task)\
            .join(TaskDataset.dataset)\
            .filter(
            filterTask,
            filterDataset,
            Paper.is_public
        )\
            .all()
        modes_res = []
        for row in models:
            current_item = (
                next((item for item in modes_res if item["id"] == row.model_id), None))
            if current_item:
                current_item[row.accuracy_type] = row.accuracy_value
            else:
                new_model = {
                    'id': row.model_id,
                    'name': row.model_name,
                    'gflops': row.model_gflops,
                    'number_of_parameters': row.model_number_of_parameters,
                    'multiply_adds': row.model_multiply_adds,
                    'operation_per_network_pass': (
                        row.model_gflops
                        if row.model_gflops else row.model_multiply_adds
                    ),
                    'hardware_burden': row.model_hardware_burden,
                    'paper_title': row.paper_title,
                    'paper_code_link': row.paper_code_link,
                    'paper_link': row.paper_link,
                    'paper_publication_date': row.paper_publication_date,
                }
                new_model[row.accuracy_type] = row.accuracy_value

                modes_res.append(new_model)

        task_dataset_res['models'] = modes_res
        return task_dataset_res

    def get_models_csv(
        self,
        db: Session, *,
        task_id: Union[int, str],
        dataset_id: Union[int, str],
    ) -> TaskDatasetModels:
        filterTask = (Task.id == task_id) if isinstance(
            task_id, int) else (Task.identifier == task_id)
        filterDataset = (Dataset.id == dataset_id) if isinstance(
            dataset_id, int) else (Dataset.identifier == dataset_id)

        models = db.query(
            Task.name.label('task_name'),
            Dataset.name.label('dataset_name'),
            Model.id.label('model_id'),
            Model.name.label('model_name'),
            Model.gflops.label('model_gflops'),
            Model.number_of_parameters.label('model_number_of_parameters'),
            Model.multiply_adds.label('model_multiply_adds'),
            Model.epochs.label('model_epochs'),
            Model.extra_training_time.label('model_extra_training_time'),
            Model.training_time.label('model_training_time'),
            Model.number_of_cpus.label('model_number_of_cpus'),
            Model.hardware_burden.label('model_hardware_burden'),
            Cpu.name.label('model_cpu'),
            Model.number_of_gpus.label('model_number_of_gpus'),
            Gpu.name.label('model_gpu'),
            Model.number_of_tpus.label('model_number_of_tpus'),
            Tpu.name.label('model_tpu'),
            AccuracyValue.value.label('accuracy_value'),
            AccuracyType.name.label('accuracy_type'),
            Paper.title.label('paper_title'),
            Paper.code_link.label('paper_code_link'),
            Paper.publication_date.label('paper_publication_date'),
            Paper.link.label('paper_link'),
        ).join(TaskDataset.models)\
            .join(Model.accuracy_values)\
            .join(AccuracyValue.accuracy_type)\
            .join(Model.paper)\
            .join(Model.cpu, isouter=True)\
            .join(Model.tpu, isouter=True)\
            .join(Model.gpu, isouter=True)\
            .join(TaskDataset.task)\
            .join(TaskDataset.dataset)\
            .filter(
            filterTask,
            filterDataset,
            Paper.is_public
        )\
            .all()
        logging.error(models)

        models_res = []
        for row in models:
            current_item = next(
                (item for item in models_res if item["model_id"] == row.model_id), None)

            if current_item:
                current_item[row.accuracy_type] = row.accuracy_value
            else:
                new_model = {
                    'task_name': row.task_name,
                    'dataset_name': row.dataset_name,
                    'model_id': row.model_id,
                    'paper_publication_date': row.paper_publication_date.year,
                    'paper_title': row.paper_title,
                    'paper_link': row.paper_link,
                    'paper_code_link': row.paper_code_link,
                    'model_name': row.model_name,
                    row.accuracy_type: row.accuracy_value,
                    'model_gflops': row.model_gflops,
                    'model_multiply_adds': row.model_multiply_adds,
                    'model_operation_per_network_pass': (
                        row.model_gflops
                        if row.model_gflops else row.model_multiply_adds
                    ),
                    'model_extra_training_time': row.model_extra_training_time,
                    'model_number_of_cpus': row.model_number_of_cpus,
                    'model_cpu': row.model_cpu,
                    'model_number_of_gpus': row.model_number_of_gpus,
                    'model_gpu': row.model_gpu,
                    'model_number_of_tpus': row.model_number_of_tpus,
                    'model_tpu': row.model_tpu,
                    'model_training_time': row.model_training_time,
                    'model_hardware_burden': row.model_hardware_burden,
                    'model_number_of_parameters': row.model_number_of_parameters,
                    'model_epochs': row.model_epochs,
                }

                models_res.append(new_model)
        return models_res


task = CRUDTask(Task)
