from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from starlette import status

from controllers.stub import Stub
from dto.schemas.request import CommonBaseQueryParamSchema
from dto.schemas.response import FAIL_RESPONSES, RESPONSE_404
from dto.task.task import TaskCreateDto, TaskMultiResponseSchema, TaskUpdateDto
from services import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get(
    "",
    response_model=None,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
    responses=FAIL_RESPONSES | RESPONSE_404,
    summary="Get tasks",
)
async def get_tasks(
    task_id: Annotated[int | None, Query(alias="id", gt=0, description="идентификатор записи в БД")] = None,
    common_params: CommonBaseQueryParamSchema = Depends(),
    service: TaskService = Depends(Stub(TaskService)),
) -> TaskMultiResponseSchema:
    return await service.get_tasks(task_id=task_id, common_params=common_params)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses=FAIL_RESPONSES,
    summary="Create task",
)
async def create_task(
    task_data: TaskCreateDto,
    service: TaskService = Depends(Stub(TaskService)),
) -> None:
    await service.create_task(task_data)


@router.put(
    "/{obj_id}",
    status_code=status.HTTP_200_OK,
    responses=FAIL_RESPONSES | RESPONSE_404,
    summary="Update task",
)
async def update_task(
    obj_id: Annotated[int, Path(gt=0, example=1, description="task id")],
    task_data: TaskUpdateDto,
    service: TaskService = Depends(Stub(TaskService)),
) -> None:
    await service.update_task(task_id=obj_id, task_data=task_data)
