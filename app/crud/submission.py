from app.utils.email import send_submission_updates_email
import json
from app.models.submission import StatusEnum
from app.models.task_dataset_accuracy_type import TaskDatasetAccuracyType
from app.models.accuracy_value import AccuracyValue
from app.models import Paper, Model
from fastapi.exceptions import HTTPException
import logging
from app.crud.base import CRUDBase
from app.schemas.submission import SubmissionData

from app.models import (Dataset, Message, Task,
                        TaskDataset, AccuracyType, Submission, Tpu, Gpu, Cpu)

from slugify import slugify


def checkDiff(oldSubmission, newSubmission):
    messages = []
    oldSubmission = oldSubmission.dict()
    newSubmission = newSubmission.dict()

    mismatch = {key for key in oldSubmission.keys(
    ) & newSubmission if oldSubmission[key] != newSubmission[key]}

    if oldSubmission['title'] != newSubmission['title']:
        messages.append('paper\'s title was changed from "{}" to "{}"'.format(
            oldSubmission['title'], newSubmission['title']))

    if oldSubmission['link'] != newSubmission['link']:
        messages.append('paper\'s link was changed from "{}" to "{}"'.format(
            oldSubmission['link'], newSubmission['link']))

    if oldSubmission['code_link'] != newSubmission['code_link']:
        messages.append('paper\'s code link was changed from "{}" to "{}"'.format(
            oldSubmission['code_link'], newSubmission['code_link']))

    if oldSubmission['publication_date'] != newSubmission['publication_date']:
        messages.append('paper\'s publication date was changed from "{}" to "{}"'.format(
            oldSubmission['publication_date'], newSubmission['publication_date']))

    if oldSubmission['authors'] != newSubmission['authors']:
        messages.append('paper\'s authors were changed from {} to {}'.format(
            ', '.join(oldSubmission['authors']), ', '.join(newSubmission['authors'])))

    if 'models' in mismatch:

        removed_models = [x for x in oldSubmission['models'] if x['name']
                          not in [model['name'] for model in newSubmission['models']]]

        for removed in removed_models:
            messages.append('{} model removed'.format(removed['name']))

        added_models = [x for x in newSubmission['models'] if x['name']
                        not in [model['name'] for model in oldSubmission['models']]]

        for added in added_models:
            messages.append('{} model added'.format(added['name']))

        possibly_modified_models = [x for x in oldSubmission['models'] if x['name'] not in [
            model['name'] for model in removed_models]]

        for possibly_modified_model in possibly_modified_models:

            model_modified = next(
                (item for item in newSubmission['models'] if item['name'] == possibly_modified_model['name']), None)

            if model_modified:

                mismatch = {key for key in possibly_modified_model.keys(
                ) & model_modified if possibly_modified_model[key] != model_modified[key]}

                for field in mismatch:
                    if field == 'accuracies':
                        removed_accuracies = [x for x in possibly_modified_model['accuracies'] if x['accuracy_type']
                                              not in [model['accuracy_type'] for model in model_modified['accuracies']]]

                        for removed in removed_accuracies:
                            messages.append('{} accuracy was removed from {}'.format(
                                removed['accuracy_type'], model_modified['name']))

                        added_accuracies = [x for x in model_modified['accuracies'] if x['accuracy_type']
                                            not in [model['accuracy_type'] for model in possibly_modified_model['accuracies']]]

                        for added in added_accuracies:
                            messages.append('{} accuracy was added to {}'.format(
                                added['accuracy_type'], model_modified['name']))

                        possibly_modified_accruacies = [x for x in possibly_modified_model['accuracies'] if x['accuracy_type'] not in [
                            accuracy['accuracy_type'] for accuracy in removed_accuracies]]

                        for accuracy_possibly_modified in possibly_modified_accruacies:
                            accuracy_modified = next(
                                (item for item in model_modified['accuracies'] if item['accuracy_type'] == accuracy_possibly_modified['accuracy_type']), None)

                            if accuracy_modified and accuracy_possibly_modified['value'] != accuracy_modified['value']:
                                messages.append('{} accuracy was changed from "{}" to "{}" on {}'.format(
                                    model_modified['name'], accuracy_modified['accuracy_type'], accuracy_possibly_modified['value'], accuracy_modified['value']))
                    else:
                        messages.append('{}\'s {} was changed from "{}" to "{}"'.format(model_modified['name'], field.replace(
                            '_', ' '), possibly_modified_model[field], model_modified[field]))
    return messages


def checkFields(db, obj_in):
    messages = []
    for model_data in obj_in.models:
        # Check if task exists
        if not db.query(Task).filter(Task.name.ilike(model_data.task)).first():
            messages.append('new task requested: "{}"'.format(model_data.task))

        # Check if dataset exists
        if not db.query(Dataset).filter(Dataset.name.ilike(model_data.dataset)).first():
            messages.append('new dataset requested: "{}"'.format(model_data.dataset))

        # Check if association between task and dataset exists
        if not db.query(TaskDataset).filter(TaskDataset.identifier == "{}-on-{}".format(
            slugify(model_data.task, max_length=45, word_boundary=True),
            slugify(model_data.dataset, max_length=45, word_boundary=True),
        )).first():
            messages.append(
                'new association beetween task and dataset requested: "{}" on "{}"'.format(
                    model_data.task, model_data.dataset))

        if model_data.cpu and not db.query(Cpu).filter(
                Cpu.name.ilike(model_data.cpu)).first():
            messages.append('new cpu requested: "{}"'.format(model_data.cpu))

        if not db.query(Gpu).filter(
                Gpu.name.ilike(model_data.gpu)).first():
            messages.append('new gpu requested: "{}"'.format(model_data.gpu))

        if model_data.tpu and not db.query(Tpu).filter(
                Tpu.name.ilike(model_data.tpu)).first():
            messages.append('new tpu requested: "{}"'.format(model_data.tpu))

        for accuracy in model_data.accuracies:
            if not db.query(AccuracyType).filter(
                    AccuracyType.name.ilike(accuracy.accuracy_type)).first():
                messages.append('new accuracy type requested: "{}" with value "{}"'.format(
                    accuracy.accuracy_type, accuracy.value))
    return messages


def calculate_hardware_burden(model):
    hw = 0
    if model.cpu and model.cpu.gflops:
        hw = hw + model.cpu.gflops * model.number_of_cpus
    if model.gpu and model.gpu.gflops:
        hw = hw + model.gpu.gflops * model.number_of_gpus
    if model.tpu and model.tpu.gflops:
        hw = hw + model.tpu.gflops * model.number_of_tpus

    hw = hw * model.training_time

    return hw if hw else None


class CRUDSubmission(CRUDBase[Submission, SubmissionData, SubmissionData]):
    def get_multi(
        self, db, *, skip: int = 0, limit: int = 100, q: str = None, owner_id, status
    ):
        submissions = db.query(Submission).filter(Submission.data.isnot(None))
        if owner_id:
            submissions = submissions.filter(Submission.owner_id == owner_id)
        if q:
            submissions = submissions.filter(
                Submission.data.as_json()['title'].as_string().ilike("%{}%".format(q)))
        if status:
            submissions = submissions.filter(Submission.status == status)

        return {
            'items': submissions.offset(skip).limit(limit).all(),
            'total': submissions.count()
        }

    def create(self, db, *, obj_in: SubmissionData, current_user):
        submission = Submission(
            data=json.loads(obj_in.json()), owner=current_user)
        messages = [Message(body="submission created", submission=submission)]
        for msg in checkFields(db, obj_in):
            messages.append(Message(body=msg, submission=submission))
        try:
            db.add(submission)
            db.commit()
            db.refresh(submission)
            return submission
        except Exception as e:
            logging.error(e)
            raise HTTPException(
                status_code=404,
                detail="Error on create submission")

    def update(self, db, *, db_obj: Submission, obj_in: SubmissionData, current_user):
        submission = db_obj
        messages = []
        for msg in checkDiff(
            SubmissionData.parse_obj(db_obj.data),
            SubmissionData.parse_obj(obj_in)
        ):
            messages.append(
                Message(
                    body="{} by {}".format(
                        msg, ' '.join([current_user.first_name, current_user.last_name])
                    ),
                    type="edit",
                    submission=submission
                )
            )
        # for msg in checkFields(db, obj_in):
        #     messages.append(Message(body=msg, submission=submission))

        submission.data = json.loads(obj_in.json())
        try:
            db.add(submission)
            db.commit()
            db.refresh(submission)
            return submission
        except Exception as e:
            logging.error(e)
            raise HTTPException(
                status_code=404,
                detail="Error on update submission")

    def update_status(self, db, *,
                      db_obj: Submission,
                      status: StatusEnum,
                      current_user,
                      background_tasks):
        submission = db_obj

        if submission.status == StatusEnum.approved:
            raise HTTPException(
                status_code=400,
                detail="Error: submission already approved")

        if status == StatusEnum.approved:
            if submission.paper:
                submission.paper.is_public = True
            else:
                updated_submission = self.process_submission(db, submission=submission,
                                                             current_user=current_user)
                message = 'We are writing to you just to let you know that your submission regarding the parper "{}" was approved.'.format(
                    submission.data.title)
                background_tasks.add_task(
                    send_submission_updates_email, email_to=submission.owner.email,
                    message=message)
                return updated_submission

        elif status == StatusEnum.declined and submission.status != StatusEnum.declined:
            submission.status = StatusEnum.declined
            if submission.paper:
                submission.paper.is_public = False
                message = 'We are writing to you just to let you know that your submission regarding the parper "{}" was declined.'.format(
                    submission.data.title)
            db.add(Message(submission=submission, body='submission status changed to "declined" by {}'.format(
                ' '.join([current_user.first_name, current_user.last_name]))))
            background_tasks.add_task(
                send_submission_updates_email, email_to=submission.owner.email,
                message=message)
        elif status == StatusEnum.need_information and submission.status != StatusEnum.need_information:
            submission.status = StatusEnum.need_information
            message = 'We are writing to you just to let you know that your submission regarding the parper "{}" is under review and that some additional information has been requested.'.format(
                submission.data.title)
            db.add(Message(submission=submission, body='submission status changed to "need information" by {}'.format(
                ' '.join([current_user.first_name, current_user.last_name]))))
            background_tasks.add_task(
                send_submission_updates_email, email_to=submission.owner.email,
                message=message)
        submission.reviewer = current_user
        db.add(submission)
        db.commit()
        db.refresh(submission)
        return submission

    def process_submission(self, db, *, submission: Submission, current_user):
        submissionData = submission.data
        submission.reviewer = current_user
        submission.status = StatusEnum.approved
        paper = Paper(
            title=submissionData['title'],
            link=submissionData['link'],
            code_link=submissionData['code_link'],
            publication_date=submissionData['publication_date'],
            authors=submissionData['authors'],
            submission=submission
        )

        for model_data in submissionData['models']:
            model = Model(
                name=model_data['name'],
                training_time=model_data['training_time'],
                gflops=model_data['gflops'],
                epochs=model_data['epochs'],
                number_of_parameters=model_data['number_of_parameters'],
                multiply_adds=model_data['multiply_adds'],
                number_of_cpus=model_data['number_of_cpus'],
                number_of_gpus=model_data['number_of_gpus'],
                number_of_tpus=model_data['number_of_tpus'],
                extra_training_time=model_data['extra_training_time']
            )

            task_dataset = db.query(TaskDataset).join(Task).join(Dataset).filter(
                Task.name == model_data['task'],
                Dataset.name == model_data['dataset']
            ).first()

            if task_dataset:
                model.task_dataset_id = task_dataset.id
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Error: association beetween task and dataset not found")

            gpu = db.query(Gpu).filter(Gpu.name.ilike(model_data['gpu'])).first()
            if gpu:
                model.gpu = gpu
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Error: gpu not found")

            if model_data['cpu']:
                cpu = db.query(Cpu).filter(Cpu.name.ilike(model_data['cpu'])).first()
                if cpu:
                    model.cpu = cpu
                else:
                    raise HTTPException(
                        status_code=404,
                        detail="Error: cpu not found")

            if model_data['tpu']:
                tpu = db.query(Tpu).filter(Tpu.name.ilike(model_data['tpu'])).first()
                if tpu:
                    model.tpu = tpu
                else:
                    raise HTTPException(
                        status_code=404,
                        detail="Error: tpu not found")

            accuracy_types_ids = []
            for accuracy in model_data['accuracies']:
                accuracy_type = db.query(AccuracyType).filter(
                    AccuracyType.name.ilike(accuracy['accuracy_type'])).first()
                if accuracy_type:
                    accuracy_types_ids.append(accuracy_type.id)
                    accuracy_value = AccuracyValue(value=accuracy['value'],
                                                   accuracy_type=accuracy_type)
                    model.accuracy_values.append(accuracy_value)
                else:
                    raise HTTPException(
                        status_code=404,
                        detail="Error: accuracy type found")
            accuracy_types_accept = db.query(TaskDatasetAccuracyType).filter(
                TaskDatasetAccuracyType.task_dataset_id == model.task_dataset_id).all()
            for accept in accuracy_types_accept:
                if accept.required and (
                        accept.accuracy_type_id not in accuracy_types_ids):
                    raise HTTPException(
                        status_code=404,
                        detail="Error: accuracy type {} is required".format(
                            accept.accuracy_type.name))
            model.hardware_burden = calculate_hardware_burden(model)
            paper.models.append(model)

        db.add(paper)
        db.add(Message(submission=submission, body='submission status changed to "approved" by {}'.format(
            ' '.join([current_user.first_name, current_user.last_name]))))
        db.commit()
        return submission


submission = CRUDSubmission(Submission)
