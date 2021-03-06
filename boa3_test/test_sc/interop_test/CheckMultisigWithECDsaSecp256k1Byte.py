from typing import List

from boa3.builtin.interop.crypto import check_multisig_with_ecdsa_secp256k1


def Main():
    pubkeys: List[bytes] = [b'123', b'456']
    assignatures: List[bytes] = [b'098', b'765']
    check_multisig_with_ecdsa_secp256k1(b'\x00\x01\x02', pubkeys, assignatures)
