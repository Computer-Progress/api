import pytest
from httpx import AsyncClient, Response

from app.main import app

submission_body = {
  "title": "foo",
  "link": "bar",
  "code_link": "foobar",
  "publication_date": "2021-09-09",
  "authors": [
    "bar foo"
  ],
  "models": [
    {
      "name": "foo",
      "task": "foofoo",
      "dataset": "foobar",
      "cpu": "bar foo",
      "gpu": "bar bar",
      "tpu": "bar",
      "gflops": 3,
      "multiply_adds": 2,
      "number_of_parameters": 20,
      "training_time": 30,
      "epochs": 5,
      "extra_training_data": True,
      "accuracies": [
        {
          "accuracy_type": "foo",
          "value": 0.1
        }
      ],
      "number_of_gpus": 3,
      "number_of_cpus": 1,
      "number_of_tpus": 2,
      "extra_training_time": False
    }
  ]
}

submission_new = {
  "title": "foo",
  "link": "bar",
  "code_link": "foobar",
  "publication_date": "2021-09-09",
  "authors": [
    "bar foo"
  ],
  "models": [
    {
      "name": "foo",
      "task": "foofoo",
      "dataset": "foobar",
      "cpu": "bar foo",
      "gpu": "bar bar",
      "tpu": "bar",
      "gflops": 3,
      "multiply_adds": 2,
      "number_of_parameters": 20,
      "training_time": 30,
      "epochs": 5,
      "extra_training_data": True,
      "accuracies": [
        {
          "accuracy_type": "foo",
          "value": 0.1
        }
      ],
      "number_of_gpus": 3,
      "number_of_cpus": 1,
      "number_of_tpus": 2,
      "extra_training_time": False
    }
  ]
}

submission_keys = {
                  "data": {**submission_body},
                  "paper_id": 0,
                  "owner_id": 0,
                  "reviewer_id": 0,
                  "status": "pending",
                  "id": 0,
                  "created_at": "2021-09-09T23:17:57.529Z",
                  "updated_at": "2021-09-09T23:17:57.529Z"
                  }

msg_res = {
  "body": "test foo bar",
  "id": 0,
  "author_id": 0,
  "submission_id": 0,
  "author": {
    "email": "user@example.com",
    "is_active": True,
    "role": "default",
    "first_name": "string",
    "last_name": "string",
    "id": 0
  },
  "type": "string"
}

@pytest.fixture(scope='module')
async def submission_created(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post('/submissions', json=submission_body)
    yield response.json()

    assert response.status_code == 200
    assert response.json().keys() == submission_keys.keys()

    async with AsyncClient(app=app,base_url=base_url, headers=headers) as ac:
        response = await ac.delete(f'/submissions/{response.json()["id"]}')

    assert response.status_code == 200
    assert response.json().keys() == submission_keys.keys()

def test_submission_post(submission_created: Response):
    created = submission_created['data']
    for key in submission_body.keys():
        assert submission_body[key] == created[key]

@pytest.mark.asyncio
async def test_submission_get_id(base_url: str, headers: dict, submission_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f'/submissions/{submission_created["id"]}')
    assert response.status_code == 200
    assert response.json().keys() == submission_keys.keys()
    assert response.json()['data'] == submission_body

@pytest.mark.asyncio
async def test_submission_get(base_url: str, headers: dict, submission_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f'/submissions')
    assert response.status_code == 200
    assert response.json()[0].keys() == submission_keys.keys()
    assert response.json()[0]['data'] == submission_body

@pytest.mark.asyncio
async def test_submission_status_put(base_url: str, headers: dict, submission_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f'/submissions/{submission_created["id"]}/status', json={"status": "declined"})
    assert response.status_code == 200
    assert response.json().keys() == submission_keys.keys()
    assert response.json()['data'] == submission_body
    assert response.json()['status'] == 'declined'

@pytest.mark.asyncio
async def test_submission_put(base_url: str, headers: dict, submission_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f'/submissions/{submission_created["id"]}', json=submission_new)
    assert response.status_code == 200
    assert response.json().keys() == submission_keys.keys()
    assert response.json()['data'] == submission_new

@pytest.mark.asyncio
async def test_submission_message_post(base_url: str, headers: dict, submission_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post(f'/submissions/{submission_created["id"]}/messages', json={'message': msg_res['body']})
    assert response.status_code == 200
    assert response.json().keys() == msg_res.keys()
    assert response.json()['body'] == msg_res['body']
    assert response.json()['author'].keys() == msg_res['author'].keys()

@pytest.mark.asyncio
async def test_submission_message_get(base_url: str, headers: dict, submission_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f'/submissions/{submission_created["id"]}/messages')
    assert response.status_code == 200
    assert response.json()[0].keys() == msg_res.keys()
    assert response.json()[0]['body'] == msg_res['body']
    assert response.json()[0]['author'].keys() == msg_res['author'].keys()
