import six
import unittest

from captaincloud.task.field import (
    FloatField, IntegerField, StringField, ByteField, BooleanField, AnyField,
    ListField, StructField, StreamField, StringStreamField, ByteStreamField
)
from captaincloud.task.field import (
    ValueField, InvalidValueException, StreamNotAvailableException
)


class TestValueFields(unittest.TestCase):
    """Tests for value fields"""

    def test_float_field(self):
        instance = FloatField()
        self.assertEqual(instance.get_initial(), None)

        self.assertEqual(instance.get(instance.set(1)), 1)
        self.assertEqual(instance.get(instance.set(1.5)), 1.5)

        with self.assertRaises(InvalidValueException):
            instance.set('ABC')

        instance = FloatField(default=2.5)
        self.assertEqual(instance.get_initial(), 2.5)

    def test_integer_field(self):
        instance = IntegerField()
        self.assertEqual(instance.get_initial(), None)

        self.assertEqual(instance.get(instance.set(1)), 1)

        with self.assertRaises(InvalidValueException):
            instance.set(1.5)

        with self.assertRaises(InvalidValueException):
            instance.set('ABC')

        instance = IntegerField(default=2)
        self.assertEqual(instance.get_initial(), 2)

    def test_string_field(self):
        instance = StringField()
        self.assertEqual(instance.get_initial(), None)

        self.assertEqual(instance.get(instance.set(six.u('ABC'))), six.u('ABC'))

        with self.assertRaises(InvalidValueException):
            instance.set(1)

        with self.assertRaises(InvalidValueException):
            instance.set(1.5)

        with self.assertRaises(InvalidValueException):
            instance.set(six.b('ABC'))

        instance = StringField(default=six.u('ABC'))
        self.assertEqual(instance.get_initial(), six.u('ABC'))

    def test_byte_field(self):
        instance = ByteField()
        self.assertEqual(instance.get_initial(), None)

        self.assertEqual(instance.get(instance.set(six.b('ABC'))), six.b('ABC'))

        with self.assertRaises(InvalidValueException):
            instance.set(1)

        with self.assertRaises(InvalidValueException):
            instance.set(1.5)

        with self.assertRaises(InvalidValueException):
            instance.set(six.u('ABC'))

        instance = ByteField(default=six.b('ABC'))
        self.assertEqual(instance.get_initial(), six.b('ABC'))

    def test_boolean_field(self):
        instance = BooleanField(default=False)
        self.assertEqual(instance.get_initial(), False)

        with self.assertRaises(InvalidValueException):
            instance.set('True')

        instance = BooleanField()
        self.assertEqual(instance.get(instance.set(True)), True)

    def test_any_field(self):
        instance = AnyField(default='hello')
        self.assertEqual(instance.get_initial(), 'hello')
        self.assertEqual(instance.get(instance.set(True)), True)

    def test_new_field(self):
        class NewField(ValueField):
            pass

        with self.assertRaises(NotImplementedError):
            instance = NewField()
            instance.set(10)

        with self.assertRaises(NotImplementedError):
            instance = NewField()
            instance.get(100)

        with self.assertRaises(NotImplementedError):
            instance = NewField()
            instance.get_initial()


class TestStreamFields(unittest.TestCase):
    """Tests for stream fields"""

    def test_string_stream(self):
        instance = StringStreamField().create()
        with self.assertRaises(StreamNotAvailableException):
            instance.write(six.u('hello'))

        with self.assertRaises(StreamNotAvailableException):
            instance.read()

        class DummyStream(object):
            def __init__(self):
                self.buffer = six.u('')

            def read(self, n=-1):
                if n == -1:
                    n = len(self.buffer)
                result = self.buffer[:n]
                self.buffer = self.buffer[n:]
                return result

            def write(self, data):
                self.buffer += data

        instance.set_real_stream(DummyStream())
        with self.assertRaises(InvalidValueException):
            instance.write(six.b('hello'))

        instance.write(six.u('hello'))
        self.assertEqual(instance.read(), six.u('hello'))

    def test_byte_stream(self):
        instance = ByteStreamField().create()
        with self.assertRaises(StreamNotAvailableException):
            instance.write(six.u('hello'))

        with self.assertRaises(StreamNotAvailableException):
            instance.read()

        class DummyStream(object):
            def __init__(self):
                self.buffer = six.b('')

            def read(self, n=-1):
                if n == -1:
                    n = len(self.buffer)
                result = self.buffer[:n]
                self.buffer = self.buffer[n:]
                return result

            def write(self, data):
                self.buffer += data

        instance.set_real_stream(DummyStream())
        with self.assertRaises(InvalidValueException):
            instance.write(six.u('hello'))

        instance.write(six.b('hello'))
        self.assertEqual(instance.read(), six.b('hello'))

        with self.assertRaises(NotImplementedError):
            StreamField().create()  # Test for coverage :)


class TestRefFields(unittest.TestCase):
    def test_list_field(self):
        instance = ListField(StringField(), default=[six.u('XYZ')])
        self.assertEqual(instance.create(), [six.u('XYZ')])

        val = instance.create()
        val.append(six.u('ABC'))
        self.assertEqual(val, [six.u('XYZ'), six.u('ABC')])

        val = instance.set([six.u('A'), six.u('B'), six.u('C')])
        self.assertEqual(val, [six.u('A'), six.u('B'), six.u('C')])

        self.assertEqual(val.pop(), six.u('C'))
        self.assertEqual(val.pop(0), six.u('A'))

        instance = ListField(FloatField())
        self.assertEqual(instance.create(), [])

        with self.assertRaises(InvalidValueException):
            instance.create().append(six.u('ABC'))

    def test_struct_field(self):
        instance = StructField(a=IntegerField(), b=FloatField())
        val = instance.create()
        val.a = 100
        val.b = 3.14
        self.assertEqual(val.a, 100)

        nested_instance = StructField(
            a=IntegerField(),
            b=StructField(
                c=FloatField()
            )
        )
        val = nested_instance.create()
        val.a = 100
        val.b.c = 3.14
        print(val.serialize())
