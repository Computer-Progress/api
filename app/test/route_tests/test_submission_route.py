import pytest
from httpx import AsyncClient, Response

from app.main import app
from app.test.utils.constants import SUBMISSION_NEW,  \
                                     SUBMISSION_BODY, \
                                     SUBMISSION_KEYS, \
                                     SUBMISSION_MSG_RES


@pytest.fixture(scope='module')
async def submission_created(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post('/submissions', json=SUBMISSION_BODY)
    yield response.json()

    assert response.status_code == 200
    assert response.json().keys() == SUBMISSION_KEYS.keys()

    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.delete(f'/submissions/{response.json()["id"]}')

    assert response.status_code == 200
    assert response.json().keys() == SUBMISSION_KEYS.keys()


def test_submission_post(submission_created: Response):
    created = submission_created['data']
    for key in SUBMISSION_BODY.keys():
        assert SUBMISSION_BODY[key] == created[key]


@pytest.mark.asyncio
async def test_submission_get_id(base_url: str,
                                 headers: dict,
                                 submission_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f'/submissions/{submission_created["id"]}')
    assert response.status_code == 200
    assert response.json().keys() == SUBMISSION_KEYS.keys()
    assert response.json()['data'] == SUBMISSION_BODY


@pytest.mark.asyncio
async def test_submission_get(base_url: str,
                              headers: dict,
                              submission_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get('/submissions')
    assert response.status_code == 200
    assert response.json()[0].keys() == SUBMISSION_KEYS.keys()
    assert response.json()[0]['data'] == SUBMISSION_BODY


@pytest.mark.asyncio
async def test_submission_status_put(base_url: str,
                                     headers: dict,
                                     submission_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f'/submissions/{submission_created["id"]}/status',
                                json={"status": "declined"})
    assert response.status_code == 200
    assert response.json().keys() == SUBMISSION_KEYS.keys()
    assert response.json()['data'] == SUBMISSION_BODY
    assert response.json()['status'] == 'declined'


@pytest.mark.asyncio
async def test_submission_put(base_url: str,
                              headers: dict,
                              submission_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f'/submissions/{submission_created["id"]}',
                                json=SUBMISSION_NEW)
    assert response.status_code == 200
    assert response.json().keys() == SUBMISSION_KEYS.keys()
    assert response.json()['data'] == SUBMISSION_NEW


@pytest.mark.asyncio
async def test_submission_message_post(base_url: str,
                                       headers: dict,
                                       submission_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post(f'/submissions/{submission_created["id"]}/messages',
                                 json={'message': SUBMISSION_MSG_RES['body']})
    assert response.status_code == 200
    assert response.json().keys() == SUBMISSION_MSG_RES.keys()
    assert response.json()['body'] == SUBMISSION_MSG_RES['body']
    assert response.json()['author'].keys() == SUBMISSION_MSG_RES['author'].keys()


@pytest.mark.asyncio
async def test_submission_message_get(base_url: str,
                                      headers: dict,
                                      submission_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f'/submissions/{submission_created["id"]}/messages')
    assert response.status_code == 200
    assert response.json()[0].keys() == SUBMISSION_MSG_RES.keys()
    assert response.json()[0]['body'] == SUBMISSION_MSG_RES['body']
    assert response.json()[0]['author'].keys() == SUBMISSION_MSG_RES['author'].keys()
