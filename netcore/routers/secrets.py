from typing import List

from fastapi import APIRouter

from netcore.externals.vault import vault
from netcore.models import Secret

router = APIRouter(prefix="/secrets", tags=["secrets"])

# TODO: Fix the vault methods in externals


@router.get("/", response_description="List all secrets", response_model=List[Secret])
def get_all_secrets(path: str):
    return vault.list_secrets(path=path)
