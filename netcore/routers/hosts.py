from typing import List
from uuid import UUID
import platform
import subprocess

from fastapi import APIRouter, BackgroundTasks

from netcore.externals.ssot import ssot
from netcore.models.hosts import Host

router = APIRouter(prefix="/hosts", tags=["hosts"])

@router.get("/", response_description="List all hosts", response_model=List[Host])
async def list_hosts():
    return [Host(status=x.status.value, name=x.name, id=x.id) for x in await ssot.client.dcim.devices.all()]


@router.get("/{id}", response_description="Get a host", response_model=Host)
async def get_host(id: UUID):
    host = ssot.client.dcim.devices.filter(id=id)[0]
    return Host(id=host.id, name=host.name, status=host.status.value)