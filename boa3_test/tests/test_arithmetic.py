from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, NotSupportedOperation
from boa3.model.operation.binaryop import BinaryOp
from boa3.model.type.type import Type
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestArithmetic(BoaTest):

    def test_addition_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/Addition.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'add', 1, 2)
        self.assertEqual(3, result)
        result = self.run_smart_contract(engine, path, 'add', -42, -24)
        self.assertEqual(-66, result)
        result = self.run_smart_contract(engine, path, 'add', -42, 24)
        self.assertEqual(-18, result)

    def test_addition_literal_operation(self):
        expected_output = (
            Opcode.PUSH3
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/AdditionLiteral.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'add_one_two')
        self.assertEqual(3, result)

    def test_addition_literal_and_variable(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.PUSH1
            + Opcode.LDARG0
            + Opcode.ADD
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/AdditionLiteralAndVariable.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'add_one', 1)
        self.assertEqual(2, result)
        result = self.run_smart_contract(engine, path, 'add_one', -10)
        self.assertEqual(-9, result)
        result = self.run_smart_contract(engine, path, 'add_one', -1)
        self.assertEqual(0, result)

    def test_addition_variable_and_literal(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.PUSH1
            + Opcode.ADD
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/AdditionVariableAndLiteral.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'add_one', 1)
        self.assertEqual(2, result)
        result = self.run_smart_contract(engine, path, 'add_one', -10)
        self.assertEqual(-9, result)
        result = self.run_smart_contract(engine, path, 'add_one', -1)
        self.assertEqual(0, result)

    def test_subtraction_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.SUB
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/Subtraction.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'sub', 10, 3)
        self.assertEqual(7, result)
        result = self.run_smart_contract(engine, path, 'sub', -42, -24)
        self.assertEqual(-18, result)
        result = self.run_smart_contract(engine, path, 'sub', -42, 24)
        self.assertEqual(-66, result)

    def test_multiplication_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.MUL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/Multiplication.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'mult', 10, 3)
        self.assertEqual(30, result)
        result = self.run_smart_contract(engine, path, 'mult', -42, -2)
        self.assertEqual(84, result)
        result = self.run_smart_contract(engine, path, 'mult', -4, 20)
        self.assertEqual(-80, result)
        result = self.run_smart_contract(engine, path, 'mult', 0, 20)
        self.assertEqual(0, result)

    def test_division_operation(self):
        path = '%s/boa3_test/test_sc/arithmetic_test/Division.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_integer_division_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.DIV
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/IntegerDivision.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'floor_div', 10, 3)
        self.assertEqual(3, result)
        result = self.run_smart_contract(engine, path, 'floor_div', -42, -9)
        self.assertEqual(4, result)
        result = self.run_smart_contract(engine, path, 'floor_div', -100, 3)
        self.assertEqual(-33, result)

    def test_modulo_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.MOD
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/Modulo.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'mod', 10, 3)
        self.assertEqual(1, result)
        result = self.run_smart_contract(engine, path, 'mod', -42, -9)
        self.assertEqual(-6, result)
        result = self.run_smart_contract(engine, path, 'mod', -100, 3)
        self.assertEqual(-1, result)

    def test_positive_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/Positive.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'plus', 10)
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'plus', -1)
        self.assertEqual(-1, result)
        result = self.run_smart_contract(engine, path, 'plus', 0)
        self.assertEqual(0, result)

    def test_negative_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.NEGATE
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/Negative.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'minus', 10)
        self.assertEqual(-10, result)
        result = self.run_smart_contract(engine, path, 'minus', -1)
        self.assertEqual(1, result)
        result = self.run_smart_contract(engine, path, 'minus', 0)
        self.assertEqual(0, result)

    def test_concatenation_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.CAT
            + Opcode.CONVERT
            + Type.str.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/Concatenation.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'concat', 'a', 'b')
        self.assertEqual('ab', result)
        result = self.run_smart_contract(engine, path, 'concat', 'unit', 'test')
        self.assertEqual('unittest', result)

    def test_power_operation(self):
        path = '%s/boa3_test/test_sc/arithmetic_test/Power.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_str_multiplication_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + BinaryOp.StrMul.bytecode
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/StringMultiplication.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'str_mult', 'a', 4)
        self.assertEqual('aaaa', result)
        result = self.run_smart_contract(engine, path, 'str_mult', 'unit', 50)
        self.assertEqual('unit' * 50, result)

    def test_mismatched_type_binary_operation(self):
        path = '%s/boa3_test/test_sc/arithmetic_test/MismatchedOperandBinary.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mismatched_type_unary_operation(self):
        path = '%s/boa3_test/test_sc/arithmetic_test/MismatchedOperandUnary.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_sequence_addition(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.PUSH4
            + Opcode.ADD
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/AdditionThreeElements.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'add_four', 1, 2)
        self.assertEqual(7, result)
        result = self.run_smart_contract(engine, path, 'add_four', -42, -24)
        self.assertEqual(-62, result)
        result = self.run_smart_contract(engine, path, 'add_four', -42, 24)
        self.assertEqual(-14, result)

    def test_sequence_addition_different_orders(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.PUSH6
            + Opcode.LDARG0
            + Opcode.ADD
            + Opcode.RET
        )
        path_1 = '%s/boa3_test/test_sc/arithmetic_test/AdditionThreeValuesUnordered1.py' % self.dirname
        output_1 = Boa3.compile(path_1)
        self.assertEqual(expected_output, output_1)

        path_2 = '%s/boa3_test/test_sc/arithmetic_test/AdditionThreeValuesUnordered2.py' % self.dirname
        output_2 = Boa3.compile(path_2)
        self.assertEqual(expected_output, output_2)

        path_3 = '%s/boa3_test/test_sc/arithmetic_test/AdditionThreeValuesUnordered3.py' % self.dirname
        output_3 = Boa3.compile(path_3)
        self.assertEqual(expected_output, output_3)

        engine = TestEngine(self.dirname)
        result_1 = self.run_smart_contract(engine, path_1, 'add_six', 5)
        result_2 = self.run_smart_contract(engine, path_2, 'add_six', 5)
        result_3 = self.run_smart_contract(engine, path_2, 'add_six', 5)
        self.assertEqual(11, result_1)
        self.assertEqual(11, result_2)
        self.assertEqual(11, result_3)

        result_1 = self.run_smart_contract(engine, path_1, 'add_six', -42)
        result_2 = self.run_smart_contract(engine, path_2, 'add_six', -42)
        result_3 = self.run_smart_contract(engine, path_2, 'add_six', -42)
        self.assertEqual(-36, result_1)
        self.assertEqual(-36, result_2)
        self.assertEqual(-36, result_3)

    def test_mixed_operations(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x05'
            + Opcode.LDARG0
            + Opcode.LDARG2
            + Opcode.LDARG4
            + Opcode.MUL        # multiplicative operations
            + Opcode.ADD        # additive operations
            + Opcode.LDARG3
            + Opcode.NEGATE     # parentheses
            + Opcode.LDARG1
            + Opcode.DIV        # multiplicative
            + Opcode.SUB        # additive
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/MixedOperations.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'mixed', 10, 20, 30, 40, 50)
        self.assertEqual(10 + 30 * 50 + 40 // 20, result)

    def test_mixed_operations_with_parentheses(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x05'
            + Opcode.LDARG0
            + Opcode.LDARG2
            + Opcode.LDARG4
            + Opcode.LDARG3
            + Opcode.NEGATE     # inside parentheses
            + Opcode.SUB        # parentheses
            + Opcode.MUL        # multiplicative operations
            + Opcode.LDARG1
            + Opcode.DIV        # multiplicative
            + Opcode.ADD        # additive operations
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/WithParentheses.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'mixed', 10, 20, 30, 40, 50)
        self.assertEqual(10 + 30 * (50 + 40) // 20, result)

    def test_addition_augmented_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.ADD
            + Opcode.STARG0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/AdditionAugmentedAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_subtraction_augmented_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.SUB
            + Opcode.STARG0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/SubtractionAugmentedAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_multiplication_augmented_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.MUL
            + Opcode.STARG0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/MultiplicationAugmentedAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_division_augmented_assignment(self):
        path = '%s/boa3_test/test_sc/arithmetic_test/DivisionAugmentedAssignment.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_integer_division_augmented_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.DIV
            + Opcode.STARG0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/IntegerDivisionAugmentedAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_modulo_augmented_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.MOD
            + Opcode.STARG0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/ModuloAugmentedAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_concatenation_augmented_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.CAT
            + Opcode.CONVERT
            + Type.str.stack_item
            + Opcode.STARG0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/ConcatenationAugmentedAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)

    def test_power_augmented_assignment(self):
        path = '%s/boa3_test/test_sc/arithmetic_test/PowerAugmentedAssignment.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_str_multiplication_operation_augmented_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + BinaryOp.StrMul.bytecode
            + Opcode.STARG0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/arithmetic_test/StringMultiplicationAugmentedAssignment.py' % self.dirname
        output = Boa3.compile(path)

        self.assertEqual(expected_output, output)
