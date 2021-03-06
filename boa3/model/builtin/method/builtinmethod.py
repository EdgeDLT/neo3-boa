import ast
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from boa3.model.builtin.builtincallable import IBuiltinCallable
from boa3.model.method import Method
from boa3.model.type.itype import IType
from boa3.model.variable import Variable


class IBuiltinMethod(IBuiltinCallable, Method, ABC):
    def __init__(self, identifier: str, args: Dict[str, Variable] = None,
                 defaults: List[ast.AST] = None, return_type: IType = None):
        super().__init__(identifier, args, defaults, return_type)

    @property
    def is_supported(self) -> bool:
        """
        Verifies if the builtin method is supported by the compiler

        :return: True if it is supported. False otherwise.
        """
        return True

    @property
    def args_on_stack(self) -> int:
        """
        Gets the number of arguments that must be on stack before the opcode is called.

        :return: the number of arguments if opcode is not empty. Zero otherwise.
        """
        if len(self.opcode) > 0:
            num_args = self._args_on_stack
            if num_args < 0:
                return 0
            elif num_args > len(self.args):
                return len(self.args)
            return num_args
        else:
            return 0

    def push_self_first(self) -> bool:
        """
        Verifies if the `self` value of the method needs to be pushed to the Neo execution stack before the
        other arguments.

        :return: a boolean value indicating if the `self` argument must be pushed before. Returns False if there isn't
                 a `self` argument in the function
        """
        return False

    def validate_self(self, self_type: IType) -> bool:
        """
        Verifies if the given value is valid to the function `self` argument

        :param self_type: type of the value
        :return: a boolean value that represents if the value is valid. Returns False if there isn't a `self` argument
                 in the function
        """
        if not self.has_self_argument:
            return False
        return self.args['self'].type.is_type_of(self_type)

    @property
    def has_self_argument(self) -> bool:
        """
        Verifies if the function has a `self` argument.

        :return: True if there is this argument. False otherwise.
        """
        return 'self' in self.args

    @property
    @abstractmethod
    def _args_on_stack(self) -> int:
        """
        Gets the number of arguments that must be on stack before the opcode is called.

        :return: the number of arguments.
        """
        return 0

    @property
    def stores_on_slot(self) -> bool:
        """
        Returns whether this method needs to update the value from a variable

        :return: whether the method needs to update a variable
        """
        return False

    @property
    def requires_reordering(self) -> bool:
        """
        Returns whether this method requires a reordering of user inputted parameters

        :return: whether the method requires the parameters to be ordered differently as inputted from the user
        """
        return False

    def reorder(self, arguments: list):
        """
        Reorder the arguments if the method requires it.

        If `requires_reordering` returns True, this method must be implemented

        :param arguments: list of arguments to be reordered
        """
        pass

    @property
    def body(self) -> Optional[str]:
        """
        Gets the body of the method.

        :return: Return the code of the method body if there is no opcode. None otherwise.
        """
        return self._body if len(self.opcode) <= 0 else None

    @property
    @abstractmethod
    def _body(self) -> Optional[str]:
        """
        Gets the body of the method.

        :return: Return the code of the method body.
        """
        return None

    def build(self, value: Any):
        """
        Creates a method instance with the given value as self

        :param value: value to build the type
        :return: The built method if the value is valid. The current object otherwise
        :rtype: IBuiltinMethod
        """
        return self
