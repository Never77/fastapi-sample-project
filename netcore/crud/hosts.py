from netcore.externals.ssot import ssot
from typing import List
from netcore.models.hosts import Host

def list_hosts() -> List[Host]:
    return [Host(id=x.id, name=x.name, status=x.status.value) for x in ssot.client.dcim.devices.all()]