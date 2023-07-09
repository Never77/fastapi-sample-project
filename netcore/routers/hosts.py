from typing import List
from uuid import UUID

from fastapi import APIRouter
from netcore.externals.ssot import ssot
from netcore.models.hosts import Host, HostIn
import ipaddress

router = APIRouter(prefix="/hosts", tags=["hosts"])


@router.get("/", response_description="List all hosts", response_model=List[Host])
async def list_hosts():
    return [
        Host(
            status=x.status.value,
            name=x.name,
            id=x.id,
            ip_addr=ipaddress.ip_interface(x.primary_ip.address),
            manufacturer=x.device_type.manufacturer.name,
        )
        for x in await ssot.client.dcim.devices.all()
    ]


@router.get("/{id}", response_description="Get a host", response_model=Host)
async def get_host(id: UUID):
    host = ssot.client.dcim.devices.filter(id=id)[0]
    print(host)
    return Host(
        id=host.id,
        name=host.name,
        status=host.status.value,
        ip_addr=ipaddress.ip_interface(host.primary_ip.address),
        manufacturer=host.device_type.manufacturer.name,
    )


# @router.post('/', response_description="Create a host", response_model=Host)
# async def create_host(host: HostIn):

#     host_ssot = ssot.client.dcim.devices.create(**host.dict())
#     return Host(manufacturer=host_ssot.device_type.manufacturer.name)
