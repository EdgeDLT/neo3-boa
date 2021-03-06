from boa3.boa3 import Boa3
from boa3.constants import ENCODING
from boa3.exception.CompilerError import (InternalError, MismatchedTypes, MissingReturnStatement, TooManyReturns,
                                          TypeHintMissing)
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestFunction(BoaTest):

    def test_integer_function(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'           # num local variables
            + b'\x01'           # num arguments
            + Opcode.PUSH10     # body
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/test_sc/function_test/IntegerFunction.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 1)
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'Main', -1)
        self.assertEqual(10, result)

    def test_string_function(self):
        expected_output = (
            # functions without arguments and local variables don't need initslot
            Opcode.PUSHDATA1        # body
            + bytes([len('42')])
            + bytes('42', ENCODING)
            + Opcode.RET            # return
        )

        path = '%s/boa3_test/test_sc/function_test/StringFunction.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual('42', result)

    def test_bool_function(self):
        expected_output = (
            # functions without arguments and local variables don't need initslot
            Opcode.PUSH1      # body
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/test_sc/function_test/BoolFunction.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(1, result)

    def test_none_function(self):
        path = '%s/boa3_test/test_sc/function_test/NoneFunction.py' % self.dirname
        self.assertCompilerLogs(InternalError, path)

    def test_arg_without_type_hint(self):
        path = '%s/boa3_test/test_sc/function_test/ArgWithoutTypeHintFunction.py' % self.dirname
        self.assertCompilerLogs(TypeHintMissing, path)

    def test_no_return_hint_function_with_empty_return_statement(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'           # num local variables
            + b'\x01'           # num arguments
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/test_sc/function_test/EmptyReturnFunction.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 5)
        self.assertEqual(None, result)

    def test_no_return_hint_function_without_return_statement(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'           # num local variables
            + b'\x01'           # num arguments
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/test_sc/function_test/NoReturnFunction.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 5)
        self.assertEqual(None, result)

    def test_return_type_hint_function_with_empty_return(self):
        path = '%s/boa3_test/test_sc/function_test/ExpectingReturnFunction.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_multiple_return_function(self):
        path = '%s/boa3_test/test_sc/function_test/MultipleReturnFunction.py' % self.dirname
        self.assertCompilerLogs(TooManyReturns, path)

    def test_tuple_function(self):
        path = '%s/boa3_test/test_sc/function_test/TupleFunction.py' % self.dirname
        self.assertCompilerLogs(TooManyReturns, path)

    def test_default_return(self):
        path = '%s/boa3_test/test_sc/function_test/DefaultReturn.py' % self.dirname
        self.assertCompilerLogs(MissingReturnStatement, path)

    def test_empty_list_return(self):
        expected_output = (
            Opcode.NEWARRAY0
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/function_test/EmptyListReturn.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([], result)

    def test_mismatched_return_type(self):
        path = '%s/boa3_test/test_sc/function_test/MismatchedReturnType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mismatched_return_type_with_if(self):
        path = '%s/boa3_test/test_sc/function_test/MismatchedReturnTypeWithIf.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_call_void_function_without_args(self):
        called_function_address = Integer(5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.CALL             # TestFunction()
            + called_function_address
            + Opcode.DROP
            + Opcode.PUSH1          # return True
            + Opcode.RET
            + Opcode.INITSLOT   # TestFunction
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH1          # a = 1
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET            # return
        )

        path = '%s/boa3_test/test_sc/function_test/CallVoidFunctionWithoutArgs.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(1, result)

    def test_call_function_without_args(self):
        called_function_address = Integer(5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x01'
            + b'\x00'
            + Opcode.CALL           # a = TestFunction()
            + called_function_address
            + Opcode.STLOC0
            + Opcode.LDLOC0         # return a
            + Opcode.RET
            + Opcode.PUSH1      # TestFunction
            + Opcode.RET            # return 1
        )

        path = '%s/boa3_test/test_sc/function_test/CallReturnFunctionWithoutArgs.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(1, result)

    def test_call_void_function_with_literal_args(self):
        called_function_address = Integer(5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.PUSH2            # TestAdd(1, 2)
            + Opcode.PUSH1
            + Opcode.CALL
            + called_function_address
            + Opcode.DROP
            + Opcode.PUSH1          # return True
            + Opcode.RET
            + Opcode.INITSLOT   # TestFunction
            + b'\x01'
            + b'\x02'
            + Opcode.LDARG0         # c = a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET            # return
        )

        path = '%s/boa3_test/test_sc/function_test/CallVoidFunctionWithLiteralArgs.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(1, result)

    def test_call_function_with_literal_args(self):
        called_function_address = Integer(5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH2          # a = TestAdd(1, 2)
            + Opcode.PUSH1
            + Opcode.CALL
            + called_function_address
            + Opcode.STLOC0
            + Opcode.LDLOC0         # return a
            + Opcode.RET
            + Opcode.INITSLOT   # TestFunction
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0         # return a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.RET            # return
        )

        path = '%s/boa3_test/test_sc/function_test/CallReturnFunctionWithLiteralArgs.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(3, result)

    def test_call_void_function_with_variable_args(self):
        called_function_address = Integer(5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH1          # a = 1
            + Opcode.STLOC0
            + Opcode.PUSH2          # b = 2
            + Opcode.STLOC1
            + Opcode.PUSH2          # TestAdd(a, b)
            + Opcode.PUSH1
            + Opcode.CALL
            + called_function_address
            + Opcode.DROP
            + Opcode.PUSH1          # return True
            + Opcode.RET
            + Opcode.INITSLOT   # TestFunction
            + b'\x01'
            + b'\x02'
            + Opcode.LDARG0         # c = a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET            # return
        )

        path = '%s/boa3_test/test_sc/function_test/CallVoidFunctionWithVariableArgs.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(1, result)

    def test_call_function_with_variable_args(self):
        called_function_address = Integer(5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x03'
            + b'\x02'
            + Opcode.PUSH1          # a = 1
            + Opcode.STLOC0
            + Opcode.PUSH2          # b = 2
            + Opcode.STLOC1
            + Opcode.PUSH2          # c = TestAdd(a, b)
            + Opcode.PUSH1
            + Opcode.CALL
            + called_function_address
            + Opcode.STLOC2
            + Opcode.LDLOC2         # return c
            + Opcode.RET
            + Opcode.INITSLOT   # TestFunction
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0         # return a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.RET            # return
        )

        path = '%s/boa3_test/test_sc/function_test/CallReturnFunctionWithVariableArgs.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        self.run_smart_contract(engine, path, 'TestAdd', 1, 2)
        self.assertEqual(1, len(engine.result_stack))
        self.assertEqual(3, engine.result_stack[-1])

    def test_call_function_on_return(self):
        called_function_address = Integer(3).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH1          # a = 1
            + Opcode.STLOC0
            + Opcode.PUSH2          # b = 2
            + Opcode.STLOC1
            + Opcode.PUSH2          # return TestAdd(a, b)
            + Opcode.PUSH1
            + Opcode.CALL
            + called_function_address
            + Opcode.RET
            + Opcode.INITSLOT   # TestFunction
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0         # return a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.RET            # return
        )

        path = '%s/boa3_test/test_sc/function_test/CallReturnFunctionOnReturn.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(3, result)

    def test_call_function_without_variables(self):
        main_to_one_address = Integer(-10).to_byte_array(min_length=1, signed=True)
        main_to_two_address = Integer(5).to_byte_array(min_length=1, signed=True)
        two_to_one_address = Integer(-24).to_byte_array(min_length=1, signed=True)
        end_if = Integer(5).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.PUSH1        # One
            + Opcode.RET            # return 1
            + Opcode.INITSLOT   # Main
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0         # if arg0 == 1
            + Opcode.PUSH1
            + Opcode.NUMEQUAL
            + Opcode.JMPIFNOT
            + end_if
            + Opcode.CALL           # return One()
            + main_to_one_address
            + Opcode.RET
            + Opcode.LDARG0         # elif arg0 == 2
            + Opcode.PUSH2
            + Opcode.NUMEQUAL
            + Opcode.JMPIFNOT
            + end_if
            + Opcode.CALL           # return Two()
            + main_to_two_address
            + Opcode.RET
            + Opcode.PUSH0          # default return
            + Opcode.RET
            + Opcode.PUSH1     # Two
            + Opcode.CALL           # return 1 + One()
            + two_to_one_address
            + Opcode.ADD
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/function_test/CallFunctionWithoutVariables.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 1)
        self.assertEqual(1, result)
        result = self.run_smart_contract(engine, path, 'Main', 2)
        self.assertEqual(2, result)
        result = self.run_smart_contract(engine, path, 'Main', 3)
        self.assertEqual(0, result)

    def test_call_function_written_before_caller(self):
        call_address = Integer(-9).to_byte_array(min_length=1, signed=True)

        expected_output = (
            Opcode.INITSLOT     # TestFunction
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0         # return a + b
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.RET
            + Opcode.PUSH2          # return TestAdd(a, b)
            + Opcode.PUSH1
            + Opcode.CALL
            + call_address
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/function_test/CallFunctionWrittenBefore.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(3, result)

    def test_return_inside_if(self):
        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # if arg0 % 3 == 1
            + Opcode.PUSH3
            + Opcode.MOD
            + Opcode.PUSH1
            + Opcode.NUMEQUAL
            + Opcode.JMPIFNOT
            + Integer(6).to_byte_array(min_length=1, signed=True)
            + Opcode.LDARG0     # return arg0 - 1
            + Opcode.PUSH1
            + Opcode.SUB
            + Opcode.RET
            + Opcode.LDARG0     # elif arg0 % 3 == 2
            + Opcode.PUSH3
            + Opcode.MOD
            + Opcode.PUSH2
            + Opcode.NUMEQUAL
            + Opcode.JMPIFNOT
            + Integer(6).to_byte_array(min_length=1, signed=True)
            + Opcode.LDARG0     # return arg0 + 1
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.RET
            + Opcode.LDARG0     # else
            + Opcode.RET            # return arg0
        )

        path = '%s/boa3_test/test_sc/function_test/ReturnIf.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 4)
        self.assertEqual(3, result)
        result = self.run_smart_contract(engine, path, 'Main', 5)
        self.assertEqual(6, result)
        result = self.run_smart_contract(engine, path, 'Main', 6)
        self.assertEqual(6, result)

    def test_missing_return_inside_if(self):
        path = '%s/boa3_test/test_sc/function_test/ReturnIfMissing.py' % self.dirname
        self.assertCompilerLogs(MissingReturnStatement, path)

    def test_missing_return_inside_elif(self):
        path = '%s/boa3_test/test_sc/function_test/ReturnElifMissing.py' % self.dirname
        self.assertCompilerLogs(MissingReturnStatement, path)

    def test_missing_return_inside_else(self):
        path = '%s/boa3_test/test_sc/function_test/ReturnElseMissing.py' % self.dirname
        self.assertCompilerLogs(MissingReturnStatement, path)

    def test_return_inside_multiple_inner_if(self):
        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # if condition
            + Opcode.JMPIFNOT
            + Integer(29).to_byte_array(min_length=1, signed=True)
            + Opcode.LDARG0     # if condition
            + Opcode.JMPIFNOT
            + Integer(14).to_byte_array(min_length=1, signed=True)
            + Opcode.LDARG0     # if condition
            + Opcode.JMPIFNOT
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH1          # return 1
            + Opcode.RET
            + Opcode.LDARG0     # if condition
            + Opcode.JMPIFNOT
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH2          # return 2
            + Opcode.RET
            + Opcode.PUSH3      # else
            + Opcode.RET            # return 3
            + Opcode.LDARG0     # elif condition
            + Opcode.JMPIFNOT
            + Integer(9).to_byte_array(min_length=1, signed=True)
            + Opcode.LDARG0     # if condition
            + Opcode.JMPIFNOT
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH4          # return 4
            + Opcode.RET
            + Opcode.PUSH5      # else
            + Opcode.RET            # return 5
            + Opcode.PUSH6      # else
            + Opcode.RET            # return 6
            + Opcode.LDARG0     # else
            + Opcode.JMPIFNOT       # if condition
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH7          # return 7
            + Opcode.RET
            + Opcode.LDARG0         # if condition
            + Opcode.JMPIFNOT
            + Integer(4).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH8          # return 8
            + Opcode.RET
            + Opcode.PUSH9          # else
            + Opcode.RET                # return 9
        )

        path = '%s/boa3_test/test_sc/function_test/ReturnMultipleInnerIf.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', True)
        self.assertEqual(1, result)
        result = self.run_smart_contract(engine, path, 'Main', False)
        self.assertEqual(9, result)

    def test_missing_return_inside_multiple_inner_if(self):
        path = '%s/boa3_test/test_sc/function_test/ReturnMultipleInnerIfMissing.py' % self.dirname
        self.assertCompilerLogs(MissingReturnStatement, path)

    def test_return_if_expression(self):
        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # return 5 if condition else 10
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH5      # 5
            + Opcode.JMP        # else
            + Integer(3).to_byte_array(min_length=1, signed=True)
            + Opcode.PUSH10     # 10
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/test_sc/function_test/ReturnIfExpression.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', True)
        self.assertEqual(5, result)
        result = self.run_smart_contract(engine, path, 'Main', False)
        self.assertEqual(10, result)

    def test_return_if_expression_mismatched_type(self):
        path = '%s/boa3_test/test_sc/function_test/ReturnIfExpressionMismatched.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_return_inside_for(self):
        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0     # for_sequence = arg0
            + Opcode.PUSH0      # for_index = 0
            + Opcode.JMP        # begin for
            + Integer(17).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER     # value = for_sequence[for_index]
            + Opcode.OVER
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return value
            + Opcode.RET
            + Opcode.INC     # for_index = for_index + 1
            + Opcode.DUP        # if for_index < len(for_sequence)
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-20).to_byte_array(min_length=1, signed=True)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.PUSH5      # else
            + Opcode.RET          # return 5
        )

        path = '%s/boa3_test/test_sc/function_test/ReturnFor.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', [1, 2, 3])
        self.assertEqual(1, result)
        result = self.run_smart_contract(engine, path, 'Main', (2, 5, 7))
        self.assertEqual(2, result)
        result = self.run_smart_contract(engine, path, 'Main', [])
        self.assertEqual(5, result)

    def test_missing_return_inside_for(self):
        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x02'
            + b'\x01'
            + Opcode.PUSH0      # x = 0
            + Opcode.STLOC0
            + Opcode.LDARG0     # for_sequence = arg0
            + Opcode.PUSH0      # for_index = 0
            + Opcode.JMP        # begin for
            + Integer(19).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER       # value = for_sequence[for_index]
            + Opcode.OVER
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.STLOC1
            + Opcode.LDLOC0     # x += value
            + Opcode.LDLOC1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.INC        # for_index = for_index + 1
            + Opcode.DUP        # if for_index < len(for_sequence)
            + Opcode.PUSH2
            + Opcode.PICK
            + Opcode.SIZE
            + Opcode.LT
            + Opcode.JMPIF
            + Integer(-22).to_byte_array(min_length=1, signed=True)
            + Opcode.DROP
            + Opcode.DROP
            + Opcode.LDLOC0     # else
            + Opcode.RET          # return x
        )

        path = '%s/boa3_test/test_sc/function_test/ReturnForOnlyOnElse.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', [1, 2, 3])
        self.assertEqual(6, result)
        result = self.run_smart_contract(engine, path, 'Main', (2, 5, 7))
        self.assertEqual(14, result)
        result = self.run_smart_contract(engine, path, 'Main', [])
        self.assertEqual(0, result)

    def test_missing_return_inside_for_else(self):
        path = '%s/boa3_test/test_sc/function_test/ReturnForElseMissing.py' % self.dirname
        self.assertCompilerLogs(MissingReturnStatement, path)

    def test_return_inside_while(self):
        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0     # x = arg0
            + Opcode.STLOC0
            + Opcode.JMP        # begin while
            + Integer(8).to_byte_array(min_length=1, signed=True)
            + Opcode.LDLOC0     # x += 1
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return x
            + Opcode.RET
            + Opcode.LDLOC0
            + Opcode.PUSH10
            + Opcode.LT
            + Opcode.JMPIF      # end while x < 10
            + Integer(-9).to_byte_array(min_length=1, signed=True)
            + Opcode.LDLOC0     # else
            + Opcode.RET            # return x
        )

        path = '%s/boa3_test/test_sc/function_test/ReturnWhile.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 5)
        self.assertEqual(6, result)
        result = self.run_smart_contract(engine, path, 'Main', 3)
        self.assertEqual(4, result)
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'Main', 100)
        self.assertEqual(100, result)

    def test_missing_return_inside_while(self):
        expected_output = (
            Opcode.INITSLOT     # Main
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0     # x = arg0
            + Opcode.STLOC0
            + Opcode.JMP        # begin while
            + Integer(6).to_byte_array(min_length=1, signed=True)
            + Opcode.LDLOC0     # x += 1
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.PUSH10
            + Opcode.LT
            + Opcode.JMPIF      # end while x < 10
            + Integer(-7).to_byte_array(min_length=1, signed=True)
            + Opcode.LDLOC0     # else
            + Opcode.RET            # return x
        )

        path = '%s/boa3_test/test_sc/function_test/ReturnWhileOnlyOnElse.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 5)
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'Main', 3)
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'Main', 100)
        self.assertEqual(100, result)

    def test_missing_return_inside_while_without_else(self):
        path = '%s/boa3_test/test_sc/function_test/ReturnWhileWithoutElse.py' % self.dirname
        self.assertCompilerLogs(MissingReturnStatement, path)

    def test_multiple_function_large_call(self):
        path = '%s/boa3_test/test_sc/function_test/MultipleFunctionLargeCall.py' % self.dirname
        engine = TestEngine(self.dirname)

        result = self.run_smart_contract(engine, path, 'main', 'calculate', [1])
        self.assertEqual(None, result)

        result = self.run_smart_contract(engine, path, 'main', 'calc', [1, 2, 3])
        self.assertEqual(None, result)

        result = self.run_smart_contract(engine, path, 'calculate', 1, [10, 3])
        self.assertEqual(13, result)
        result = self.run_smart_contract(engine, path, 'main', 'calculate', [1, 10, 3])
        self.assertEqual(13, result)

        result = self.run_smart_contract(engine, path, 'calculate', 2, [10, 3])
        self.assertEqual(7, result)
        result = self.run_smart_contract(engine, path, 'main', 'calculate', [2, 10, 3])
        self.assertEqual(7, result)

        result = self.run_smart_contract(engine, path, 'calculate', 3, [10, 3])
        self.assertEqual(3, result)
        result = self.run_smart_contract(engine, path, 'main', 'calculate', [3, 10, 3])
        self.assertEqual(3, result)

        result = self.run_smart_contract(engine, path, 'calculate', 4, [10, 3])
        self.assertEqual(30, result)
        result = self.run_smart_contract(engine, path, 'main', 'calculate', [4, 10, 3])
        self.assertEqual(30, result)

        result = self.run_smart_contract(engine, path, 'calculate', 5, [10, 3])
        self.assertEqual(1, result)
        result = self.run_smart_contract(engine, path, 'main', 'calculate', [5, 10, 3])
        self.assertEqual(1, result)

    def test_function_with_default_argument(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH3  # x = add(1, 2, 3)
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.CALL
            + Integer(14).to_byte_array(signed=True, min_length=1)
            + Opcode.STLOC0
            + Opcode.PUSH0
            + Opcode.PUSH6  # y = add(5, 6)
            + Opcode.PUSH5
            + Opcode.CALL
            + Integer(8).to_byte_array(signed=True, min_length=1)
            + Opcode.STLOC1
            + Opcode.LDLOC1
            + Opcode.LDLOC0
            + Opcode.PUSH2
            + Opcode.PACK
            + Opcode.RET
            + Opcode.INITSLOT   # def add(a: int, b: int, c: int = 0)
            + b'\x00\x03'
            + Opcode.LDARG0     # return a + b + c
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.LDARG2
            + Opcode.ADD
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/function_test/FunctionWithDefaultArgument.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([6, 11], result)

    def test_function_with_only_default_arguments(self):
        expected_output = (
            Opcode.PUSH0        # defaults
            + Opcode.PUSH0
            + Opcode.PUSH0
            + Opcode.CALL   # add()
            + Integer(20).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH0      # defaults
            + Opcode.PUSH6      # add(5, 6)
            + Opcode.PUSH5
            + Opcode.CALL
            + Integer(15).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH0      # defaults
            + Opcode.PUSH0
            + Opcode.PUSH9      # add(9)
            + Opcode.CALL
            + Integer(10).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH3      # add(1, 2, 3)
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.CALL
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.RET
            + Opcode.INITSLOT   # def add(a: int, b: int, c: int)
            + b'\x00\x03'
            + Opcode.LDARG0     # return a + b + c
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.LDARG2
            + Opcode.ADD
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/function_test/FunctionWithOnlyDefaultArguments.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([6, 9, 11, 0], result)

    def test_function_with_default_argument_between_other_args(self):
        path = '%s/boa3_test/test_sc/function_test/FunctionWithDefaultArgumentBetweenArgs.py' % self.dirname

        with self.assertRaises(SyntaxError):
            output = Boa3.compile(path)

    def test_call_function_with_kwargs(self):
        path = '%s/boa3_test/test_sc/function_test/CallFunctionWithKwargs.py' % self.dirname
        self.assertCompilerLogs(InternalError, path)
