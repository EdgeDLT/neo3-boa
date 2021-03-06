from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, NotSupportedOperation
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestRelational(BoaTest):

    def test_number_equality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NUMEQUAL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/NumEquality.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 1, 2)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 2)
        self.assertEqual(True, result)

    def test_number_inequality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NUMNOTEQUAL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/NumInequality.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 1, 2)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 2)
        self.assertEqual(False, result)

    def test_number_inequality_operation_2(self):
        path = '%s/boa3_test/test_sc/relational_test/NumInequalityPython2.py' % self.dirname

        with self.assertRaises(SyntaxError):
            output = Boa3.compile(path)

    def test_number_less_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.LT
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/NumLessThan.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 1, 2)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 2)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 1)
        self.assertEqual(False, result)

    def test_number_less_or_equal_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.LE
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/NumLessOrEqual.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 1, 2)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 2)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 1)
        self.assertEqual(False, result)

    def test_number_greater_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.GT
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/NumGreaterThan.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 1, 2)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 2)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 1)
        self.assertEqual(True, result)

    def test_number_greater_or_equal_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.GE
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/NumGreaterOrEqual.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 1, 2)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 2)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 1)
        self.assertEqual(True, result)

    def test_identity_operation(self):
        path = '%s/boa3_test/test_sc/relational_test/NumIdentity.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_boolean_equality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NUMEQUAL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/BoolEquality.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', True, False)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', True, True)
        self.assertEqual(True, result)

    def test_boolean_inequality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NUMNOTEQUAL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/BoolInequality.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', True, False)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', True, True)
        self.assertEqual(False, result)

    def test_multiple_comparisons(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x03'
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.LE
            + Opcode.LDARG0
            + Opcode.LDARG2
            + Opcode.LE
            + Opcode.BOOLAND
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/NumRange.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 1, 2, 5)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 1, 5)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 5, 1, 2)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 2, 5, 1)
        self.assertEqual(False, result)

    def test_string_equality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.EQUAL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/StrEquality.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'test')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'unit')
        self.assertEqual(True, result)

    def test_string_inequality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NOTEQUAL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/StrInequality.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'test')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'unit')
        self.assertEqual(False, result)

    def test_string_less_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.LT
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/StrLessThan.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 'test', 'unit')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'unit')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'test')
        self.assertEqual(True, result)

    def test_string_less_or_equal_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.LE
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/StrLessOrEqual.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 'test', 'unit')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'unit')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'test')
        self.assertEqual(True, result)

    def test_string_greater_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.GT
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/StrGreaterThan.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 'test', 'unit')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'unit')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'test')
        self.assertEqual(False, result)

    def test_string_greater_or_equal_than_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.GE
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/StrGreaterOrEqual.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 'test', 'unit')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'unit')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 'unit', 'test')
        self.assertEqual(False, result)

    def test_mixed_equality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.EQUAL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/MixedEquality.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 1, 'unit')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 123, '123')
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', Integer.from_bytes(b'123'), '123')
        self.assertEqual(False, result)

    def test_mixed_inequality_operation(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.LDARG1
            + Opcode.NOTEQUAL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/relational_test/MixedInequality.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 1, 'unit')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 123, '123')
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', Integer.from_bytes(b'123'), '123')
        self.assertEqual(True, result)

    def test_mixed_less_than_operation(self):
        path = '%s/boa3_test/test_sc/relational_test/MixedLessThan.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mixed_less_or_equal_than_operation(self):
        path = '%s/boa3_test/test_sc/relational_test/MixedLessOrEqual.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mixed_greater_than_operation(self):
        path = '%s/boa3_test/test_sc/relational_test/MixedGreaterThan.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mixed_greater_or_equal_than_operation(self):
        path = '%s/boa3_test/test_sc/relational_test/MixedGreaterOrEqual.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)
