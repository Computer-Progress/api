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

    task = db.query(models.Task).filter(
        models.Task.name == 'Machine Translation').first()
    if not task:
        task = models.Task(name='Machine Translation')

    dataset = models.Dataset(name='WMT2014 English-French')

    BLEU = models.AccuracyType(name='BLEU')
    SACREBLEU = models.AccuracyType(name='SACREBLEU')

    task_dataset_accuracy_type_BLEU = models.TaskDatasetAccuracyType(
        required=True, main=True, accuracy_type=BLEU)
    task_dataset_accuracy_type_SACREBLEU = models.TaskDatasetAccuracyType(
        required=False, main=False, accuracy_type=SACREBLEU)

    task_dataset = models.TaskDataset()
    task_dataset.dataset = dataset
    task_dataset.accuracy_types.append(task_dataset_accuracy_type_BLEU)
    task_dataset.accuracy_types.append(task_dataset_accuracy_type_SACREBLEU)

    task.datasets.append(task_dataset)

    with open('app/database/seeders/wmt2014_en_fr.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        papers = {}
        for row in csv_reader:
            if papers.get(row.get('title')):
                papers[row.get('title')].append(row)
            else:
                papers[row.get('title')] = [row]

        for _, p in papers.items():
            paper = {
                'title': p[0].get('title'),
                'link': p[0].get('paper'),
                'code_link': p[0].get('authors implementation'),
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
                        (parseFloat(m.get('#flops')) / 10e9) if (
                            parseFloat(m.get('#flops'))) else None,
                    'epochs':  parseInt(m.get('#epochs')),
                    'number_of_parameters':  parseInt(m.get('#param')),
                    'multiply_adds':  parseFloat(m.get('#multiply-adds')),
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

                model.hardware_burden = calculate_hardware_burden(model)

                models.AccuracyValue(
                    value=parseFloat(m.get('BLEU')),
                    accuracy_type=BLEU,
                    model=model
                )
                models.AccuracyValue(
                    value=parseFloat(m.get('SACREBLEU')),
                    accuracy_type=SACREBLEU,
                    model=model
                )
                task_dataset.models.append(model)
        db.add(task)
        db.commit()
