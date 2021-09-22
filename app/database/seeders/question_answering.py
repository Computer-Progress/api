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

    task = models.Task(name='Question Answering', identifier='question-answering',
                       description='Question Answering is the task of answering questions (typically reading comprehension questions), but abstaining when presented with a question that cannot be answered based on the provided context.',
                       image='https://computerprogress.xyz/image/question-answering.svg')

    dataset = models.Dataset(name='SQuAD 1.1', identifier='squad11')

    F1 = models.AccuracyType(name='F1')
    EM = models.AccuracyType(name='EM')

    task_dataset_accuracy_type_F1 = models.TaskDatasetAccuracyType(
        required=True, main=True, accuracy_type=F1)
    task_dataset_accuracy_type_EM = models.TaskDatasetAccuracyType(
        required=False, main=False, accuracy_type=EM)

    task_dataset = models.TaskDataset(task=task, dataset=dataset)

    task_dataset.accuracy_types.append(task_dataset_accuracy_type_F1)
    task_dataset.accuracy_types.append(task_dataset_accuracy_type_EM)
    if os.path.exists('app/database/seeders/data/PaperWithCode_Integration_Data_NLP_Question_Answering_SQuAD_1_1.csv'):
        with open('app/database/seeders/data/PaperWithCode_Integration_Data_NLP_Question_Answering_SQuAD_1_1.csv', mode='r') as csv_file:
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
                        'epochs':  parseInt(m.get('#epochs')),
                        'number_of_parameters':  parseInt(m.get('#params')),
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
                        accuracy_type=F1,
                        model=model
                    )
                    models.AccuracyValue(
                        value=parseFloat(m.get('EM')),
                        accuracy_type=EM,
                        model=model
                    )
                    task_dataset.models.append(model)
        db.add(task_dataset)
        db.commit()
