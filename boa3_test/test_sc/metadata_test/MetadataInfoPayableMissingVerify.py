from boa3.builtin import metadata, NeoMetadata


def Main() -> int:
    return 5


@metadata
def payable_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.is_payable = True
    return meta