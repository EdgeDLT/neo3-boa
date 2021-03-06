from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class Sha256Method(InteropMethod):
    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'sha256'
        syscall = 'Neo.Crypto.SHA256'
        args: Dict[str, Variable] = {'key': Variable(Type.any)}
        super().__init__(identifier, syscall, args, return_type=Type.bytes)
