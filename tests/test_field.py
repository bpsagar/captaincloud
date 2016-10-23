import unittest
from captaincloud.task.field import FloatField, IntegerField, StringField
from captaincloud.task.field import ValueField, InvalidValueException


class TestFields(unittest.TestCase):
    """Tests for fields"""

    def test_float_input(self):
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

    def test_integer_input(self):
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

    def test_string_input(self):
        instance = StringField()
        self.assertEqual(instance.get(), None)

        instance.set('ABC')
        self.assertEqual(instance.get(), 'ABC')

        with self.assertRaises(InvalidValueException):
            instance.set(1)

        with self.assertRaises(InvalidValueException):
            instance.set(1.5)

        instance = StringField(default='ABC')
        self.assertEqual(instance.get(), 'ABC')

    def test_new_input(self):

        class NewField(ValueField):
            pass

        with self.assertRaises(NotImplementedError):
            instance = NewField()
            instance.set(10)

        with self.assertRaises(NotImplementedError):
            instance = NewField()
            instance.get()
