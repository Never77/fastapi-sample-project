from typing import List

from fastapi import APIRouter

from netcore.externals.vault import vault
from netcore.models import Account

router = APIRouter(prefix="/secrets", tags=["secrets"])

# TODO: Fix the vault methods in externals


@router.get("/", response_description="List all secrets", response_model=List[Account])  # Only to simplify example
def get_all_secrets(mount_point: str):
    return vault.list_secrets(mount_point=mount_point)
