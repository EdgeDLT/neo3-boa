from typing import Dict, List, Optional, Tuple

from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class GetNeoScriptHashMethod(IBuiltinMethod):
    def __init__(self):
        from boa3.model.type.type import Type
        identifier = '-get_neo'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=Type.bytes)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.type.type import Type
        from boa3.neo.vm.type.Integer import Integer

        value = b'\xde\x5f\x57\xd4\x30\xd3\xde\xce\x51\x1c\xf9\x75\xa8\xd3\x78\x48\xcb\x9e\x05\x25'
        return [
            (Opcode.PUSHDATA1, Integer(len(value)).to_byte_array() + value),
            (Opcode.CONVERT, Type.bytes.stack_item)
        ]


class NeoProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'NEO'
        getter = GetNeoScriptHashMethod()
        super().__init__(identifier, getter)
