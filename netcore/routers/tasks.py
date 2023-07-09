from celery.result import AsyncResult
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from netcore.utils.worker import create_task

router = APIRouter(prefix="/tasks", tags=["celery"])


@router.post("/", status_code=201)
def run_task(payload=Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@router.get("/{id}")
def get_status(id: str):
    task_result = AsyncResult(id)
    result = {"task_id": id, "task_status": task_result.status, "task_result": task_result.result}

    return JSONResponse(result)
