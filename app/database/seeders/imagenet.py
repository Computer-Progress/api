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

    task = models.Task(name='Image Classification', identifier='image-classification',
                       description='Image Classification is a fundamental task that attempts to comprehend an entire image as a whole. The goal is to classify the image by assigning it to a specific label. Typically, Image Classification refers to images in which only one object appears and is analyzed. In contrast, object detection involves both classification and localization tasks, and is used to analyze more realistic cases in which multiple objects may exist in an image.',
                       image='http://ec2-3-129-18-205.us-east-2.compute.amazonaws.com/image/image-classification.svg')

    dataset = models.Dataset(name='Imagenet', identifier='imagenet')

    top1 = models.AccuracyType(name='top1_error')
    top5 = models.AccuracyType(name='top5_error')

    task_dataset_accuracy_type_top1 = models.TaskDatasetAccuracyType(
        required=True, main=True, accuracy_type=top1)
    task_dataset_accuracy_type_top5 = models.TaskDatasetAccuracyType(
        required=False, main=False, accuracy_type=top5)

    task_dataset = models.TaskDataset(task=task, dataset=dataset)

    task_dataset.accuracy_types.append(task_dataset_accuracy_type_top1)
    task_dataset.accuracy_types.append(task_dataset_accuracy_type_top5)

    with open('app/database/seeders/imagenet.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        papers = {}
        for row in csv_reader:
            if papers.get(row.get('paper')):
                papers[row.get('paper')].append(row)
            else:
                papers[row.get('paper')] = [row]

        for _, p in papers.items():
            paper = {
                'title': p[0].get('paper'),
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
                    'name':  m.get('model'),
                    'training_time': parseInt(m.get('time_sec')),
                    'gflops':
                        (parseFloat(m.get('flops')) / 10e9) if (
                            parseFloat(m.get('flops'))) else None,
                    'epochs':  parseInt(m.get('#epochs')),
                    'number_of_parameters':  parseInt(m.get('#params')),
                    'multiply_adds':  parseFloat(m.get('multiadds')),
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
                    value=parseFloat(m.get('top1_error')),
                    accuracy_type=top1,
                    model=model
                )
                models.AccuracyValue(
                    value=parseFloat(m.get('top5_error')),
                    accuracy_type=top5,
                    model=model
                )
                task_dataset.models.append(model)
        db.add(task_dataset)
        db.commit()
