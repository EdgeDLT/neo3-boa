from boa3.builtin import NeoMetadata, metadata
from boa3.builtin.interop.storage import delete


def Main(key: int):
    delete(key)


@metadata
def manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.has_storage = True
    return meta
