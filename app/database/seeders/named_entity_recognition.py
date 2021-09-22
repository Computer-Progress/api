from datetime import datetime
import os

from fastapi.encoders import jsonable_encoder
from app import models, schemas
import csv
from app.database.session import SessionLocal
from app.database.seeders.helper import parseFloat, parseInt, calculate_hardware_burden


def check_none(value):
    if isinstance(value, int) or isinstance(value, float):
        return value
    return 0


def get_date(year):
    if parseInt(year):
        return datetime(year=int(year), month=6, day=15)
    return None




def seed() -> None:
    db = SessionLocal()

    task = models.Task(name='Named Entity Recognition',
                       identifier='named-entity-recognition',
                       description='Named entity recognition (NER) is the task of tagging entities in text with their corresponding type. Approaches typically use BIO notation, which differentiates the beginning (B) and the inside (I) of entities. O is used for non-entity tokens.',
                       image='https://computerprogress.xyz/image/named-entity-recognition.svg')

    dataset = models.Dataset(name='Conll 2003', identifier='conll-2003')
    f1_score = models.AccuracyType(name='F1')

    task_dataset_accuracy_type_f1_score = models.TaskDatasetAccuracyType(
        required=True, main=True, accuracy_type=f1_score)

    task_dataset = models.TaskDataset(task=task, dataset=dataset)

    task_dataset.accuracy_types.append(task_dataset_accuracy_type_f1_score)
    if os.path.exists('app/database/seeders/data/PaperWithCode_Integration_Data_NLP_Named_Entity_Recognition_CoNLL.csv'):
        with open('app/database/seeders/data/PaperWithCode_Integration_Data_NLP_Named_Entity_Recognition_CoNLL.csv', mode='r') as csv_file:
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
                    'link': p[0].get('paper_url'),
                    'pwc_link': p[0].get('pwc_url'),
                    'code_link': p[0].get('code_link'),
                    'publication_date': get_date(p[0].get('year')),
                    'authors': p[0].get('authors'),
                }
                paper = models.Paper(**paper)
                paper.submission = models.Submission(status='approved')

                count = 0
                for m in p:
                    count += 1

                    model = {
                        'name':  m.get('method').strip() if m.get('method') else None,
                        'training_time': parseInt(m.get('time_sec')),
                        'gflops':
                            (parseFloat(m.get('flops')) / 10e9) if (
                                parseFloat(m.get('flops'))) else None,
                        'epochs':  parseInt(m.get('epochs')),
                        'number_of_parameters':  parseInt(m.get('number_of_parameters')),
                        'multiply_adds':
                            (parseFloat(m.get('multiply_adds')) / 10e9) if (
                                parseFloat(m.get('multiply_adds'))) else None,
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
                            models.Cpu.name.ilike(m.get('cpu'))).first()
                    if m.get('gpu'):
                        model.gpu = db.query(models.Gpu).filter(
                            models.Gpu.name.ilike(m.get('gpu'))).first()
                    if m.get('tpu'):
                        model.tpu = db.query(models.Tpu).filter(
                            models.Tpu.name.ilike(m.get('tpu'))).first()

                    hardware_burden = calculate_hardware_burden(model)
                    model.hardware_burden = hardware_burden if hardware_burden != 0 else None

                    models.AccuracyValue(
                        value=parseFloat(m.get('F1')),
                        accuracy_type=f1_score,
                        model=model
                    )

                    task_dataset.models.append(model)
        db.add(task_dataset)
        db.commit()
