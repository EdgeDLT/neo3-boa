from boa3.builtin import metadata, NeoMetadata


def Main() -> int:
    return 5


@metadata
def storage_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.has_storage = 1
    return meta