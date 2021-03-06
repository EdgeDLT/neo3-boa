from boa3.boa3 import Boa3
from boa3.builtin.interop.contract import GAS, NEO
from boa3.builtin.interop.runtime import TriggerType
from boa3.exception.CompilerError import MismatchedTypes, UnexpectedArgument, UnfilledArgument
from boa3.exception.CompilerWarning import NameShadowing
from boa3.model.builtin.interop.interop import Interop
from boa3.model.type.type import Type
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestInterop(BoaTest):

    def test_check_witness(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.CheckWitness.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CheckWitness.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_witness_imported_as(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.CheckWitness.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CheckWitnessImportedAs.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_witness_mismatched_type(self):
        path = '%s/boa3_test/test_sc/interop_test/CheckWitnessMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_notify_str(self):
        event_name = String('notify').to_bytes()
        message = 'str'
        string = String(message).to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/NotifyStr.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        self.run_smart_contract(engine, path, 'Main')
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=Interop.Notify.name)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((message,), event_notifications[0].arguments)

    def test_notify_int(self):
        event_name = String('notify').to_bytes()
        expected_output = (
            Opcode.PUSH15
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/NotifyInt.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        self.run_smart_contract(engine, path, 'Main')
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=Interop.Notify.name)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((15,), event_notifications[0].arguments)

    def test_notify_bool(self):
        event_name = String('notify').to_bytes()
        expected_output = (
            Opcode.PUSH1
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/NotifyBool.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        self.run_smart_contract(engine, path, 'Main')
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=Interop.Notify.name)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((1,), event_notifications[0].arguments)

    def test_notify_none(self):
        event_name = String('notify').to_bytes()
        expected_output = (
            Opcode.PUSHNULL
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/NotifyNone.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        self.run_smart_contract(engine, path, 'Main')
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=Interop.Notify.name)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual((None,), event_notifications[0].arguments)

    def test_notify_sequence(self):
        event_name = String('notify').to_bytes()
        expected_output = (
            Opcode.PUSH7
            + Opcode.PUSH5
            + Opcode.PUSH3
            + Opcode.PUSH2
            + Opcode.PUSH4
            + Opcode.PACK
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(event_name)).to_byte_array(min_length=1)
            + event_name
            + Opcode.SYSCALL
            + Interop.Notify.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/NotifySequence.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        self.run_smart_contract(engine, path, 'Main')
        self.assertGreater(len(engine.notifications), 0)

        event_notifications = engine.get_events(event_name=Interop.Notify.name)
        self.assertEqual(1, len(event_notifications))
        self.assertEqual(([2, 3, 5, 7],), event_notifications[0].arguments)

    def test_log_mismatched_type(self):
        path = '%s/boa3_test/test_sc/interop_test/LogMismatchedValueInt.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_log_str(self):
        string = String('str').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.SYSCALL
            + Interop.Log.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/LogStr.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_get_trigger(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.GetTrigger.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/Trigger.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(TriggerType.APPLICATION, result)

    def test_is_application_trigger(self):
        application = Integer(TriggerType.APPLICATION.value).to_byte_array()
        expected_output = (
            Opcode.SYSCALL
            + Interop.GetTrigger.interop_method_hash
            + Opcode.PUSHDATA1
            + Integer(len(application)).to_byte_array(min_length=1)
            + application
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.EQUAL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/TriggerApplication.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(True, result)

    def test_is_verification_trigger(self):
        verification = Integer(TriggerType.VERIFICATION.value).to_byte_array()
        expected_output = (
            Opcode.SYSCALL
            + Interop.GetTrigger.interop_method_hash
            + Opcode.PUSHDATA1
            + Integer(len(verification)).to_byte_array(min_length=1)
            + verification
            + Opcode.CONVERT
            + Type.int.stack_item
            + Opcode.EQUAL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/TriggerVerification.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(False, result)

    def test_get_calling_script_hash(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.CallingScriptHash.getter.interop_method_hash
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CallingScriptHash.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_calling_script_hash_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CallingScriptHashCantAssign.py' % self.dirname
        output = self.assertCompilerLogs(NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_call_contract(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x03'
            + Opcode.LDARG2
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CallScriptHash.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        call_contract_path = '%s/boa3_test/test_sc/arithmetic_test/Addition.py' % self.dirname
        Boa3.compile_and_save(call_contract_path)

        contract, manifest = self.get_output(call_contract_path)
        manifest_hash = manifest['abi']['hash']
        call_hash = Integer(manifest_hash[2:], 16).to_byte_array()
        call_contract_path = call_contract_path.replace('.py', '.nef')

        engine = TestEngine(self.dirname)
        with self.assertRaises(TestExecutionException, msg=self.CALLED_CONTRACT_DOES_NOT_EXIST_MSG):
            self.run_smart_contract(engine, path, 'Main', call_hash, 'add', [1, 2])
        engine.add_contract(call_contract_path)

        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'add', [1, 2])
        self.assertEqual(3, result)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'add', [-42, -24])
        self.assertEqual(-66, result)
        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'add', [-42, 24])
        self.assertEqual(-18, result)

    def test_call_contract_without_args(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x02'
            + Opcode.NEWARRAY0
            + Opcode.LDARG1
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CallScriptHashWithoutArgs.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        call_contract_path = '%s/boa3_test/test_sc/list_test/IntList.py' % self.dirname
        Boa3.compile_and_save(call_contract_path)

        contract, manifest = self.get_output(call_contract_path)
        manifest_hash = manifest['abi']['hash']
        call_hash = Integer(manifest_hash[2:], 16).to_byte_array()
        call_contract_path = call_contract_path.replace('.py', '.nef')

        engine = TestEngine(self.dirname)
        with self.assertRaises(TestExecutionException, msg=self.CALLED_CONTRACT_DOES_NOT_EXIST_MSG):
            self.run_smart_contract(engine, path, 'Main', call_hash, 'Main')
        engine.add_contract(call_contract_path)

        result = self.run_smart_contract(engine, path, 'Main', call_hash, 'Main')
        self.assertEqual([1, 2, 3], result)

    def test_call_contract_too_many_parameters(self):
        path = '%s/boa3_test/test_sc/interop_test/CallScriptHashTooManyArguments.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_call_contract_too_few_parameters(self):
        path = '%s/boa3_test/test_sc/interop_test/CallScriptHashTooFewArguments.py' % self.dirname
        self.assertCompilerLogs(UnfilledArgument, path)

    def test_get_neo_native_script_hash(self):
        value = NEO
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(value)).to_byte_array()
            + value
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/NeoScriptHash.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(value, result)

    def test_neo_native_script_hash_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/NeoScriptHashCantAssign.py' % self.dirname
        output = self.assertCompilerLogs(NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_gas_native_script_hash(self):
        value = GAS
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(value)).to_byte_array()
            + value
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/GasScriptHash.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(value, result)

    def test_gas_native_script_hash_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/GasScriptHashCantAssign.py' % self.dirname
        output = self.assertCompilerLogs(NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_block_time(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.BlockTime.getter.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/BlockTime.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(0, result)

    def test_block_time_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/BlockTimeCantAssign.py' % self.dirname
        output = self.assertCompilerLogs(NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_current_height(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.CurrentHeight.getter.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CurrentHeight.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_current_height_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CurrentHeightCantAssign.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_get_gas_left(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.GasLeft.getter.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/GasLeft.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_gas_left_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/GasLeftCantAssign.py' % self.dirname
        output = self.assertCompilerLogs(NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_get_invocation_counter(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.InvocationCounter.getter.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/InvocationCounter.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_invocation_counter_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/InvocationCounterCantAssign.py' % self.dirname
        output = self.assertCompilerLogs(NameShadowing, path)
        self.assertEqual(expected_output, output)

    def test_ripemd160_str(self):
        string = String('test').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.SYSCALL
            + Interop.Ripemd160.interop_method_hash
            + Opcode.DROP
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/Ripemd160Str.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_hash160_str(self):
        string = String('test').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.SYSCALL
            + Interop.Sha256.interop_method_hash
            + Opcode.SYSCALL
            + Interop.Ripemd160.interop_method_hash
            + Opcode.DROP
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/Hash160Str.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_sha256_str(self):
        string = String('test').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.SYSCALL
            + Interop.Sha256.interop_method_hash
            + Opcode.DROP
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/Sha256Str.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_hash256_str(self):
        string = String('test').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.SYSCALL
            + Interop.Sha256.interop_method_hash
            + Opcode.SYSCALL
            + Interop.Sha256.interop_method_hash
            + Opcode.DROP
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/Hash256Str.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_base58_encode(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.Base58Encode.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/Base58Encode.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        import base58
        engine = TestEngine(self.dirname)
        expected_result = base58.b58encode('unit test')
        result = self.run_smart_contract(engine, path, 'Main', 'unit test')
        if isinstance(result, str):
            result = String(result).to_bytes()
        self.assertEqual(expected_result, result)

        expected_result = base58.b58encode('')
        result = self.run_smart_contract(engine, path, 'Main', '')
        if isinstance(result, str):
            result = String(result).to_bytes()
        self.assertEqual(expected_result, result)

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        expected_result = base58.b58encode(long_string)
        result = self.run_smart_contract(engine, path, 'Main', long_string)
        if isinstance(result, str):
            result = String(result).to_bytes()
        self.assertEqual(expected_result, result)

    def test_base58_encode_mismatched_type(self):
        path = '%s/boa3_test/test_sc/interop_test/Base58EncodeMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_base58_decode(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.Base58Decode.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/Base58Decode.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        import base58
        engine = TestEngine(self.dirname)
        arg = base58.b58encode('unit test')
        result = self.run_smart_contract(engine, path, 'Main', arg)
        self.assertEqual('unit test', result)

        arg = base58.b58encode('')
        result = self.run_smart_contract(engine, path, 'Main', arg)
        self.assertEqual('', result)

        long_string = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan magna eu massa '
                       'vulputate bibendum. Aliquam commodo euismod tristique. Sed purus erat, pretium ut interdum '
                       'et, aliquet sed mauris. Curabitur vitae turpis euismod, hendrerit mi a, rhoncus justo. Mauris '
                       'sollicitudin, nisl sit amet feugiat pharetra, odio ligula congue tellus, vel pellentesque '
                       'libero leo id dui. Morbi vel risus vehicula, consectetur mauris eget, gravida ligula. '
                       'Maecenas aliquam velit sit amet nisi ultricies, ac sollicitudin nisi mollis. Lorem ipsum '
                       'dolor sit amet, consectetur adipiscing elit. Ut tincidunt, nisi in ullamcorper ornare, '
                       'est enim dictum massa, id aliquet justo magna in purus.')
        arg = base58.b58encode(long_string)
        result = self.run_smart_contract(engine, path, 'Main', arg)
        self.assertEqual(long_string, result)

    def test_base58_decode_mismatched_type(self):
        path = '%s/boa3_test/test_sc/interop_test/Base58DecodeMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_check_multisig_with_ecdsa_secp256r1_str(self):
        string = String('test').to_bytes()
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()

        expected_output = (
                Opcode.INITSLOT
                + b'\x02'
                + b'\x00'
                + Opcode.PUSHDATA1
                + Integer(len(byte_input1)).to_byte_array(min_length=1)
                + byte_input1
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input0)).to_byte_array(min_length=1)
                + byte_input0
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC0
                + Opcode.PUSHDATA1
                + Integer(len(byte_input3)).to_byte_array(min_length=1)
                + byte_input3
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input2)).to_byte_array(min_length=1)
                + byte_input2
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC1
                + Opcode.LDLOC1
                + Opcode.LDLOC0
                + Opcode.PUSHDATA1
                + Integer(len(string)).to_byte_array(min_length=1)
                + string
                + Opcode.SYSCALL
                + Interop.CheckMultisigWithECDsaSecp256r1.interop_method_hash
                + Opcode.DROP
                + Opcode.PUSHNULL
                + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CheckMultisigWithECDsaSecp256r1Str.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_multisig_with_ecdsa_secp256r1_int(self):
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()

        expected_output = (
                Opcode.INITSLOT
                + b'\x02'
                + b'\x00'
                + Opcode.PUSHDATA1
                + Integer(len(byte_input1)).to_byte_array(min_length=1)
                + byte_input1
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input0)).to_byte_array(min_length=1)
                + byte_input0
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC0
                + Opcode.PUSHDATA1
                + Integer(len(byte_input3)).to_byte_array(min_length=1)
                + byte_input3
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input2)).to_byte_array(min_length=1)
                + byte_input2
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC1
                + Opcode.LDLOC1
                + Opcode.LDLOC0
                + Opcode.PUSH10
                + Opcode.SYSCALL
                + Interop.CheckMultisigWithECDsaSecp256r1.interop_method_hash
                + Opcode.DROP
                + Opcode.PUSHNULL
                + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CheckMultisigWithECDsaSecp256r1Int.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_multisig_with_ecdsa_secp256r1_bool(self):
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()

        expected_output = (
                Opcode.INITSLOT
                + b'\x02'
                + b'\x00'
                + Opcode.PUSHDATA1
                + Integer(len(byte_input1)).to_byte_array(min_length=1)
                + byte_input1
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input0)).to_byte_array(min_length=1)
                + byte_input0
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC0
                + Opcode.PUSHDATA1
                + Integer(len(byte_input3)).to_byte_array(min_length=1)
                + byte_input3
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input2)).to_byte_array(min_length=1)
                + byte_input2
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC1
                + Opcode.LDLOC1
                + Opcode.LDLOC0
                + Opcode.PUSH0
                + Opcode.SYSCALL
                + Interop.CheckMultisigWithECDsaSecp256r1.interop_method_hash
                + Opcode.DROP
                + Opcode.PUSHNULL
                + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CheckMultisigWithECDsaSecp256r1Bool.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_multisig_with_ecdsa_secp256r1_byte(self):
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()
        byte_input4 = b'\x00\x01\x02'

        expected_output = (
                Opcode.INITSLOT
                + b'\x02'
                + b'\x00'
                + Opcode.PUSHDATA1
                + Integer(len(byte_input1)).to_byte_array(min_length=1)
                + byte_input1
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input0)).to_byte_array(min_length=1)
                + byte_input0
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC0
                + Opcode.PUSHDATA1
                + Integer(len(byte_input3)).to_byte_array(min_length=1)
                + byte_input3
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input2)).to_byte_array(min_length=1)
                + byte_input2
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC1
                + Opcode.LDLOC1
                + Opcode.LDLOC0
                + Opcode.PUSHDATA1
                + Integer(len(byte_input4)).to_byte_array(min_length=1)
                + byte_input4
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.SYSCALL
                + Interop.CheckMultisigWithECDsaSecp256r1.interop_method_hash
                + Opcode.DROP
                + Opcode.PUSHNULL
                + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CheckMultisigWithECDsaSecp256r1Byte.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_multisig_with_ecdsa_secp256k1_str(self):
        string = String('test').to_bytes()
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()

        expected_output = (
                Opcode.INITSLOT
                + b'\x02'
                + b'\x00'
                + Opcode.PUSHDATA1
                + Integer(len(byte_input1)).to_byte_array(min_length=1)
                + byte_input1
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input0)).to_byte_array(min_length=1)
                + byte_input0
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC0
                + Opcode.PUSHDATA1
                + Integer(len(byte_input3)).to_byte_array(min_length=1)
                + byte_input3
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input2)).to_byte_array(min_length=1)
                + byte_input2
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC1
                + Opcode.LDLOC1
                + Opcode.LDLOC0
                + Opcode.PUSHDATA1
                + Integer(len(string)).to_byte_array(min_length=1)
                + string
                + Opcode.SYSCALL
                + Interop.CheckMultisigWithECDsaSecp256k1.interop_method_hash
                + Opcode.DROP
                + Opcode.PUSHNULL
                + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CheckMultisigWithECDsaSecp256k1Str.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_multisig_with_ecdsa_secp256k1_int(self):
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()

        expected_output = (
                Opcode.INITSLOT
                + b'\x02'
                + b'\x00'
                + Opcode.PUSHDATA1
                + Integer(len(byte_input1)).to_byte_array(min_length=1)
                + byte_input1
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input0)).to_byte_array(min_length=1)
                + byte_input0
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC0
                + Opcode.PUSHDATA1
                + Integer(len(byte_input3)).to_byte_array(min_length=1)
                + byte_input3
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input2)).to_byte_array(min_length=1)
                + byte_input2
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC1
                + Opcode.LDLOC1
                + Opcode.LDLOC0
                + Opcode.PUSH10
                + Opcode.SYSCALL
                + Interop.CheckMultisigWithECDsaSecp256k1.interop_method_hash
                + Opcode.DROP
                + Opcode.PUSHNULL
                + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CheckMultisigWithECDsaSecp256k1Int.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_multisig_with_ecdsa_secp256k1_bool(self):
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()

        expected_output = (
                Opcode.INITSLOT
                + b'\x02'
                + b'\x00'
                + Opcode.PUSHDATA1
                + Integer(len(byte_input1)).to_byte_array(min_length=1)
                + byte_input1
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input0)).to_byte_array(min_length=1)
                + byte_input0
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC0
                + Opcode.PUSHDATA1
                + Integer(len(byte_input3)).to_byte_array(min_length=1)
                + byte_input3
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input2)).to_byte_array(min_length=1)
                + byte_input2
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC1
                + Opcode.LDLOC1
                + Opcode.LDLOC0
                + Opcode.PUSH0
                + Opcode.SYSCALL
                + Interop.CheckMultisigWithECDsaSecp256k1.interop_method_hash
                + Opcode.DROP
                + Opcode.PUSHNULL
                + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CheckMultisigWithECDsaSecp256k1Bool.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_check_multisig_with_ecdsa_secp256k1_byte(self):
        byte_input0 = String('123').to_bytes()
        byte_input1 = String('456').to_bytes()
        byte_input2 = String('098').to_bytes()
        byte_input3 = String('765').to_bytes()
        byte_input4 = b'\x00\x01\x02'

        expected_output = (
                Opcode.INITSLOT
                + b'\x02'
                + b'\x00'
                + Opcode.PUSHDATA1
                + Integer(len(byte_input1)).to_byte_array(min_length=1)
                + byte_input1
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input0)).to_byte_array(min_length=1)
                + byte_input0
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC0
                + Opcode.PUSHDATA1
                + Integer(len(byte_input3)).to_byte_array(min_length=1)
                + byte_input3
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSHDATA1
                + Integer(len(byte_input2)).to_byte_array(min_length=1)
                + byte_input2
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.PUSH2
                + Opcode.PACK
                + Opcode.STLOC1
                + Opcode.LDLOC1
                + Opcode.LDLOC0
                + Opcode.PUSHDATA1
                + Integer(len(byte_input4)).to_byte_array(min_length=1)
                + byte_input4
                + Opcode.CONVERT
                + Type.bytes.stack_item
                + Opcode.SYSCALL
                + Interop.CheckMultisigWithECDsaSecp256k1.interop_method_hash
                + Opcode.DROP
                + Opcode.PUSHNULL
                + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/CheckMultisigWithECDsaSecp256k1Byte.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)
