import pytest
from typing import Any
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.routes.user import router
from app.main import app


client = TestClient(router)

base_url='http://localhost:8000/api/v1'

user_id = []

@pytest.mark.asyncio
async def test_user_creation():
  body = {
    "email": "barbar@foofoo.com",
    "first_name": "Foo",
    "last_name": "bar",
    "password": "foobar"
  }  
  async with AsyncClient(app=app, base_url=base_url) as ac:
    response = await ac.post('/users/open', json=body)
  print(response.json())
  user_id = response.json()
  assert response.status_code == 200
  assert list(response.json().keys()) == [
                              'email',
                              'is_active',
                              'role',
                              'first_name',
                              'last_name',
                              'id'
                              ]

@pytest.mark.asyncio
async def test_user_get():
  async with AsyncClient(app=app, base_url=base_url) as ac:
    response = await ac.get(f'/users/{user_id.id}')
  print(user_id)
  assert response.status_code == 200
  assert response.json() == user_id
