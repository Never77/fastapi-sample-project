from typing import List

from netcore.externals.ssot import ssot
from netcore.models.hosts import Host


def list_hosts() -> List[Host]:
    return [
        Host(
            id=x.id,
            name=x.name,
            status=x.status.value,
            address=x.primary_ip.address if x.primary_ip else None,
            manufacturer=x.device_type.manufacturer.name,
        )
        for x in ssot.client.dcim.devices.all()
    ]
