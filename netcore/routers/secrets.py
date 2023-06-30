from fastapi import APIRouter, Depends
from netcore.models import Secret
from typing import List
from netcore.models.backends import APIBackend
from netcore.externals.vault import vault

router = APIRouter(prefix="/secrets", tags=["secrets"])

# TODO: Fix the vault methods in externals

@router.get("/", response_description="List all secrets", response_model=List[Secret])
def get_all_secrets(path: str):
    return vault.list_secrets(path=path)
