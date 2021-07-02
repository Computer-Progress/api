from datetime import datetime

from fastapi.encoders import jsonable_encoder
from app import models, schemas
import csv
from app.database.session import SessionLocal
from app.database.seeders.helper import parseFloat, parseInt


def check_none(value):
    if isinstance(value, int) or isinstance(value, float):
        return value
    return 0


def get_date(year):
    if parseInt(year):
        return datetime(year=int(year), month=6, day=15)
    return None


def calculate_hardware_burden(model):
    return (
        (check_none(model.tpu.gflops) if model.tpu else 0) *
        check_none(model.number_of_tpus) +
        (check_none(model.gpu.gflops) if model.gpu else 0) *
        check_none(model.number_of_gpus) +
        (check_none(model.cpu.gflops) if model.cpu else 0) *
        check_none(model.number_of_cpus)
    ) * check_none(model.training_time)


def seed() -> None:
    db = SessionLocal()

    task = models.Task(name='Object Detection', identifier='object-detection',
                       description='Object detection is the task of detecting instances of objects of a certain class within an image. The state-of-the-art methods can be categorized into two main types: one-stage methods and two stage-methods. One-stage methods prioritize inference speed, and example models include YOLO, SSD and RetinaNet. Two-stage methods prioritize detection accuracy, and example models include Faster R-CNN, Mask R-CNN and Cascade R-CNN. The most popular benchmark is the MSCOCO dataset. Models are typically evaluated according to a Mean Average Precision metric.',
                       image='http: // ec2-3-129-18-205.us-east-2.compute.amazonaws.com/image/object-detection.svg'
                       )

    dataset = models.Dataset(name='MS COCO', identifier='ms-coco')

    box_ap = models.AccuracyType(name='BOX AP')
    ap50 = models.AccuracyType(name='AP50')
    ap75 = models.AccuracyType(name='AP75')
    aps = models.AccuracyType(name='APS')
    apm = models.AccuracyType(name='APM')
    apl = models.AccuracyType(name='APL')

    task_dataset_accuracy_type_box_ap = models.TaskDatasetAccuracyType(
        required=True, main=True, accuracy_type=box_ap)
    task_dataset_accuracy_type_ap50 = models.TaskDatasetAccuracyType(
        required=False, main=False, accuracy_type=ap50)
    task_dataset_accuracy_type_ap75 = models.TaskDatasetAccuracyType(
        required=False, main=False, accuracy_type=ap75)
    task_dataset_accuracy_type_aps = models.TaskDatasetAccuracyType(
        required=False, main=False, accuracy_type=aps)
    task_dataset_accuracy_type_apm = models.TaskDatasetAccuracyType(
        required=False, main=False, accuracy_type=apm)
    task_dataset_accuracy_type_apl = models.TaskDatasetAccuracyType(
        required=False, main=False, accuracy_type=apl)

    task_dataset = models.TaskDataset(task=task, dataset=dataset)

    task_dataset.accuracy_types.append(task_dataset_accuracy_type_box_ap)
    task_dataset.accuracy_types.append(task_dataset_accuracy_type_ap50)
    task_dataset.accuracy_types.append(task_dataset_accuracy_type_ap75)
    task_dataset.accuracy_types.append(task_dataset_accuracy_type_aps)
    task_dataset.accuracy_types.append(task_dataset_accuracy_type_apm)
    task_dataset.accuracy_types.append(task_dataset_accuracy_type_apl)

    with open('app/database/seeders/ms_coco.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        papers = {}
        for row in csv_reader:
            if papers.get(row.get('paper')):
                papers[row.get('paper')].append(row)
            else:
                papers[row.get('paper')] = [row]

        for _, p in papers.items():
            paper = {
                'title': p[0].get('title'),
                'link': p[0].get('url'),
                'code_link': p[0].get('code_link'),
                'publication_date': get_date(p[0].get('year')),
                'authors': p[0].get('authors'),
            }
            paper = models.Paper(**paper)
            paper.revision = models.Revision(status='approved')

            count = 0
            for m in p:
                count += 1

                model = {
                    'name':  m.get('method'),
                    'training_time': parseInt(m.get('time_sec')),
                    'gflops':
                        (parseFloat(m.get('flops')) / 10e9) if (
                            parseFloat(m.get('flops'))) else None,
                    'epochs':  parseInt(m.get('#epochs')),
                    'number_of_parameters':  parseInt(m.get('#param')),
                    'multiply_adds':
                        (parseFloat(m.get('multiadds')) / 10e9) if (
                            parseFloat(m.get('multiadds'))) else None,
                    'number_of_cpus':  parseInt(m.get('#cpu')),
                    'number_of_gpus':  parseInt(m.get('#gpu')),
                    'number_of_tpus':  parseInt(m.get('#tpu')),
                }
                try:

                    model = jsonable_encoder(model)
                    schemas.Model(**model)
                except Exception:

                    continue
                model = models.Model(**model)

                model.paper = paper

                if m.get('cpu'):
                    model.cpu = db.query(models.Cpu).filter(
                        models.Cpu.name == m.get('cpu')).first()
                if m.get('gpu'):
                    model.gpu = db.query(models.Gpu).filter(
                        models.Gpu.name == m.get('gpu')).first()
                if m.get('tpu'):
                    model.tpu = db.query(models.Tpu).filter(
                        models.Tpu.name == m.get('tpu')).first()

                hardware_burden = calculate_hardware_burden(model)
                model.hardware_burden = hardware_burden if hardware_burden != 0 else None

                models.AccuracyValue(
                    value=parseFloat(m.get('BOX_AP')),
                    accuracy_type=box_ap,
                    model=model
                )
                models.AccuracyValue(
                    value=parseFloat(m.get('AP50')),
                    accuracy_type=ap50,
                    model=model
                )
                models.AccuracyValue(
                    value=parseFloat(m.get('AP75')),
                    accuracy_type=ap75,
                    model=model
                )
                models.AccuracyValue(
                    value=parseFloat(m.get('APS')),
                    accuracy_type=aps,
                    model=model
                )
                models.AccuracyValue(
                    value=parseFloat(m.get('APM')),
                    accuracy_type=apm,
                    model=model
                )
                models.AccuracyValue(
                    value=parseFloat(m.get('APL')),
                    accuracy_type=apl,
                    model=model
                )
                task_dataset.models.append(model)
        db.add(task_dataset)
        db.commit()
