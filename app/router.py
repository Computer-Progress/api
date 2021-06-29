from fastapi import APIRouter
from app.routes import (accuracy_type, login, model, user,
                        cpu, tpu, gpu, task, dataset, paper, util, sota, paper_with_code_integration)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(task.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(sota.router, prefix="/sota", tags=["sota"])
api_router.include_router(model.router, prefix="/models", tags=["models"])
api_router.include_router(dataset.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(paper.router, prefix="/papers", tags=["papers"])
api_router.include_router(accuracy_type.router,
                          prefix="/accuracy_types", tags=["accuracy types"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(cpu.router, prefix="/cpus", tags=["cpus"])
api_router.include_router(tpu.router, prefix="/tpus", tags=["tpus"])
api_router.include_router(gpu.router, prefix="/gpus", tags=["gpus"])
api_router.include_router(util.router, prefix="/utils", tags=["utils"])
api_router.include_router(paper_with_code_integration.router, prefix="/metrics",
                          tags=["paper with code integration"])
