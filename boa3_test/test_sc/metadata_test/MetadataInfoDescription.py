from boa3.builtin import NeoMetadata, metadata


def Main() -> int:
    return 5


@metadata
def description_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.description = 'This is an example'
    return meta
