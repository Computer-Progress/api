from .test_db import TestSessionLocal

def override_get_db() :
  try:
    db = TestSessionLocal()
    yield db
  finally:
    db.close()