from netcore.externals.vault import vault

def list_secrets(mount_point: str):
    return vault.list_secrets(mount_point=mount_point)