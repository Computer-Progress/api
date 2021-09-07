import pytest
from typing import Any
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.routes.user import router
from app.main import app


client = TestClient(router)



@pytest.mark.asyncio
async def test_user_route(headers, base_url):
  user_id = []
  body = {
    "email": "barbar@foofoo.com",
    "first_name": "Foo",
    "last_name": "bar",
    "password": "foobar"
  }  
  async with AsyncClient(app=app, base_url=base_url) as ac:
    response = await ac.post('/users/open', json=body)
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
  async with AsyncClient(app=app, base_url=base_url) as ac:
    response = await ac.get(f'/users/{user_id["id"]}', headers=headers)
  assert response.status_code == 200
  assert response.json() == user_id
