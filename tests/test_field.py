import six
import unittest

from captaincloud.task.field import (
    FloatField, IntegerField, StringField, ByteField, BooleanField
)
from captaincloud.task.field import ValueField, InvalidValueException


class TestFields(unittest.TestCase):
    """Tests for fields"""

    def test_float_field(self):
        instance = FloatField()
        self.assertEqual(instance.get(), None)

        instance.set(1)
        self.assertEqual(instance.get(), 1)

        instance.set(1.5)
        self.assertEqual(instance.get(), 1.5)

        with self.assertRaises(InvalidValueException):
            instance.set('ABC')

        instance = FloatField(default=2.5)
        self.assertEqual(instance.get(), 2.5)

        instance1 = FloatField(default=2.5)
        instance2 = instance1.clone()
        self.assertEqual(instance1.get(), instance2.get())
        instance1.set(4.0)
        self.assertNotEqual(instance1.get(), instance2.get())

    def test_integer_field(self):
        instance = IntegerField()
        self.assertEqual(instance.get(), None)

        instance.set(1)
        self.assertEqual(instance.get(), 1)

        with self.assertRaises(InvalidValueException):
            instance.set(1.5)

        with self.assertRaises(InvalidValueException):
            instance.set('ABC')

        instance = IntegerField(default=2)
        self.assertEqual(instance.get(), 2)

    def test_string_field(self):
        instance = StringField()
        self.assertEqual(instance.get(), None)

        instance.set(six.u('ABC'))
        self.assertEqual(instance.get(), six.u('ABC'))

        with self.assertRaises(InvalidValueException):
            instance.set(1)

        with self.assertRaises(InvalidValueException):
            instance.set(1.5)

        with self.assertRaises(InvalidValueException):
            instance.set(six.b('ABC'))

        instance = StringField(default=six.u('ABC'))
        self.assertEqual(instance.get(), six.u('ABC'))

    def test_byte_field(self):
        instance = ByteField()
        self.assertEqual(instance.get(), None)

        instance.set(six.b('ABC'))
        self.assertEqual(instance.get(), six.b('ABC'))

        with self.assertRaises(InvalidValueException):
            instance.set(1)

        with self.assertRaises(InvalidValueException):
            instance.set(1.5)

        with self.assertRaises(InvalidValueException):
            instance.set(six.u('ABC'))

        instance = ByteField(default=six.b('ABC'))
        self.assertEqual(instance.get(), six.b('ABC'))

    def test_boolean_field(self):
        instance = BooleanField(default=False)
        self.assertEqual(instance.get(), False)

        with self.assertRaises(InvalidValueException):
            instance.set('True')

        instance = BooleanField()
        instance.set(True)
        self.assertEqual(instance.get(), True)

    def test_new_field(self):
        class NewField(ValueField):
            pass

        with self.assertRaises(NotImplementedError):
            instance = NewField()
            instance.set(10)

        with self.assertRaises(NotImplementedError):
            instance = NewField()
            instance.get()
