from boa3.boa3 import Boa3
from boa3.exception.CompilerError import (InternalError, MismatchedTypes, UnexpectedArgument, UnfilledArgument,
                                          UnresolvedOperation)
from boa3.model.type.type import Type
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest


class TestRange(BoaTest):

    RANGE_ERROR_MESSAGE = String('range() arg 3 must not be zero').to_bytes()

    def test_range_given_length(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.PUSH1      # range(arg0)
            + Opcode.PUSH0
            + Opcode.LDARG0
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/test_sc/range_test/RangeGivenLen.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_range_given_start(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.PUSH1      # range(arg0, arg1)
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/test_sc/range_test/RangeGivenStart.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_range_given_step(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x03'
            + Opcode.LDARG2     # range(arg0, arg1, arg2)
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/test_sc/range_test/RangeGivenStep.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_range_parameter_mismatched_type(self):
        path = '%s/boa3_test/test_sc/range_test/RangeParameterMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_range_as_sequence(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.PUSH1      # range(arg0, arg1)
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/test_sc/range_test/RangeExpectedSequence.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_range_mismatched_type(self):
        path = '%s/boa3_test/test_sc/range_test/RangeMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_range_too_few_parameters(self):
        path = '%s/boa3_test/test_sc/range_test/RangeTooFewParameters.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)

    def test_range_too_many_parameters(self):
        path = '%s/boa3_test/test_sc/range_test/RangeTooManyParameters.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_range_get_value(self):
        path = '%s/boa3_test/test_sc/range_test/GetValue.py' % self.dirname

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_range_set_value(self):
        path = '%s/boa3_test/test_sc/range_test/SetValue.py' % self.dirname
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_range_slicing(self):
        from boa3.model.type.type import Type
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH1      # range(6)
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[2:3]
            + Opcode.PUSH2
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PUSH3
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PUSH2      # get slice
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.MIN        # slice end
            + Opcode.NEWARRAY0  # slice
            + Opcode.PUSH2
            + Opcode.PICK       # index
            + Opcode.JMP        # while index < end
            + Integer(32).to_byte_array(min_length=1)
            + Opcode.DUP            # if index >= slice start
            + Opcode.PUSH4
            + Opcode.PICK
            + Opcode.GE
            + Opcode.JMPIFNOT
            + Integer(25).to_byte_array(min_length=1)
            + Opcode.OVER               # slice.append(array[index])
            + Opcode.PUSH5
            + Opcode.PICK
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.OVER
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.CAT
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.APPEND
            + Opcode.INC            # index += 1
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.LT
            + Opcode.JMPIF          # end while index < slice end
            + Integer(-34).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.REVERSE4
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/range_test/RangeSlicingLiteralValues.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_range_slicing_with_variables(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH2      # a1 = 2
            + Opcode.STLOC0
            + Opcode.PUSH3      # a2 = 3
            + Opcode.STLOC1
            + Opcode.PUSH1      # range(6)
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.STLOC2
            + Opcode.LDLOC2     # return a[a1:a2]
            + Opcode.PUSH2
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PUSH3
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PUSH2      # get slice
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.MIN        # slice end
            + Opcode.NEWARRAY0  # slice
            + Opcode.PUSH2
            + Opcode.PICK       # index
            + Opcode.JMP        # while index < end
            + Integer(32).to_byte_array(min_length=1)
            + Opcode.DUP            # if index >= slice start
            + Opcode.PUSH4
            + Opcode.PICK
            + Opcode.GE
            + Opcode.JMPIFNOT
            + Integer(25).to_byte_array(min_length=1)
            + Opcode.OVER               # slice.append(array[index])
            + Opcode.PUSH5
            + Opcode.PICK
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.OVER
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.CAT
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.APPEND
            + Opcode.INC            # index += 1
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.LT
            + Opcode.JMPIF          # end while index < slice end
            + Integer(-34).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.REVERSE4
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/range_test/RangeSlicingVariableValues.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_range_slicing_negative_start(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH1      # range(6)
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[-4:]
            + Opcode.DUP
            + Opcode.SIZE       # slice end
            + Opcode.PUSH4
            + Opcode.NEGATE
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.SWAP       # get slice
            + Opcode.NEWARRAY0  # slice
            + Opcode.PUSH2
            + Opcode.PICK       # index
            + Opcode.JMP        # while index < end
            + Integer(32).to_byte_array(min_length=1)
            + Opcode.DUP            # if index >= slice start
            + Opcode.PUSH4
            + Opcode.PICK
            + Opcode.GE
            + Opcode.JMPIFNOT
            + Integer(25).to_byte_array(min_length=1)
            + Opcode.OVER               # slice.append(array[index])
            + Opcode.PUSH5
            + Opcode.PICK
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.OVER
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.CAT
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.APPEND
            + Opcode.INC            # index += 1
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.LT
            + Opcode.JMPIF          # end while index < slice end
            + Integer(-34).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.REVERSE4
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/range_test/RangeSlicingNegativeStart.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_range_slicing_negative_end(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH1      # range(6)
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[:-4]
            + Opcode.PUSH4
            + Opcode.NEGATE         # slice end
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PUSH0
            + Opcode.SWAP
            + Opcode.NEWARRAY0  # slice
            + Opcode.PUSH2
            + Opcode.PICK       # index
            + Opcode.JMP        # while index < end
            + Integer(32).to_byte_array(min_length=1)
            + Opcode.DUP            # if index >= slice start
            + Opcode.PUSH4
            + Opcode.PICK
            + Opcode.GE
            + Opcode.JMPIFNOT
            + Integer(25).to_byte_array(min_length=1)
            + Opcode.OVER               # slice.append(array[index])
            + Opcode.PUSH5
            + Opcode.PICK
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.OVER
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.CAT
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.APPEND
            + Opcode.INC            # index += 1
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.LT
            + Opcode.JMPIF          # end while index < slice end
            + Integer(-34).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.REVERSE4
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/range_test/RangeSlicingNegativeEnd.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_range_slicing_start_omitted(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH1      # range(6)
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[:3]
            + Opcode.PUSH3          # slice end
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PUSH0
            + Opcode.SWAP
            + Opcode.NEWARRAY0  # slice
            + Opcode.PUSH2
            + Opcode.PICK       # index
            + Opcode.JMP        # while index < end
            + Integer(32).to_byte_array(min_length=1)
            + Opcode.DUP            # if index >= slice start
            + Opcode.PUSH4
            + Opcode.PICK
            + Opcode.GE
            + Opcode.JMPIFNOT
            + Integer(25).to_byte_array(min_length=1)
            + Opcode.OVER               # slice.append(array[index])
            + Opcode.PUSH5
            + Opcode.PICK
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.OVER
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.CAT
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.APPEND
            + Opcode.INC            # index += 1
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.LT
            + Opcode.JMPIF          # end while index < slice end
            + Integer(-34).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.REVERSE4
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/range_test/RangeSlicingStartOmitted.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_range_slicing_omitted(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH1      # range(6)
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[:]
            + Opcode.UNPACK
            + Opcode.PACK
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/range_test/RangeSlicingOmitted.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_range_slicing_end_omitted(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH1      # range(6)
            + Opcode.PUSH0
            + Opcode.PUSH6
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.JMPIF
            + Integer(5 + len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSHDATA1
            + Integer(len(self.RANGE_ERROR_MESSAGE)).to_byte_array(signed=True, min_length=1)
            + self.RANGE_ERROR_MESSAGE
            + Opcode.THROW
            + Opcode.NEWARRAY0
            + Opcode.REVERSE4
            + Opcode.SWAP
            + Opcode.JMP
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.OVER
            + Opcode.APPEND
            + Opcode.OVER
            + Opcode.ADD
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.SIGN
            + Opcode.PUSH0
            + Opcode.JMPGT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.GT
            + Opcode.JMP
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-19).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a[2:]
            + Opcode.DUP
            + Opcode.SIZE       # slice end
            + Opcode.PUSH2
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.SWAP       # get slice
            + Opcode.NEWARRAY0  # slice
            + Opcode.PUSH2
            + Opcode.PICK       # index
            + Opcode.JMP        # while index < end
            + Integer(32).to_byte_array(min_length=1)
            + Opcode.DUP            # if index >= slice start
            + Opcode.PUSH4
            + Opcode.PICK
            + Opcode.GE
            + Opcode.JMPIFNOT
            + Integer(25).to_byte_array(min_length=1)
            + Opcode.OVER               # slice.append(array[index])
            + Opcode.PUSH5
            + Opcode.PICK
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.OVER
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.CAT
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.APPEND
            + Opcode.INC            # index += 1
            + Opcode.DUP
            + Opcode.PUSH3
            + Opcode.PICK
            + Opcode.LT
            + Opcode.JMPIF          # end while index < slice end
            + Integer(-34).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.REVERSE4
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.RET        # return
        )
        path = '%s/boa3_test/test_sc/range_test/RangeSlicingEndOmitted.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_range_slicing_omitted_stride(self):
        path = '%s/boa3_test/test_sc/range_test/RangeSlicingWithStride.py' % self.dirname
        self.assertCompilerLogs(InternalError, path)

    def test_range_slicing_omitted_with_stride(self):
        path = '%s/boa3_test/test_sc/range_test/RangeSlicingOmittedWithStride.py' % self.dirname
        self.assertCompilerLogs(InternalError, path)
