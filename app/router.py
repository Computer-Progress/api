from fastapi import APIRouter

from app.routes import login, user, cpu, tpu, gpu

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(cpu.router, prefix="/cpus", tags=["cpus"])
api_router.include_router(tpu.router, prefix="/tpus", tags=["tpus"])
api_router.include_router(gpu.router, prefix="/gpus", tags=["gpus"])
