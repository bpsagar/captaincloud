import unittest
from captaincloud.task.input import FloatInput, IntegerInput, StringInput
from captaincloud.task.input import ValueInput
from captaincloud.task.mixin import InvalidValueException


class TestInput(unittest.TestCase):
    """Tests for inputs"""

    def test_float_input(self):
        instance = FloatInput()
        self.assertEqual(instance.get(), None)

        instance.set(1)
        self.assertEqual(instance.get(), 1)

        instance.set(1.5)
        self.assertEqual(instance.get(), 1.5)

        with self.assertRaises(InvalidValueException):
            instance.set('ABC')

        instance = FloatInput(default=2.5)
        self.assertEqual(instance.get(), 2.5)

    def test_integer_input(self):
        instance = IntegerInput()
        self.assertEqual(instance.get(), None)

        instance.set(1)
        self.assertEqual(instance.get(), 1)

        with self.assertRaises(InvalidValueException):
            instance.set(1.5)

        with self.assertRaises(InvalidValueException):
            instance.set('ABC')

        instance = IntegerInput(default=2)
        self.assertEqual(instance.get(), 2)

    def test_string_input(self):
        instance = StringInput()
        self.assertEqual(instance.get(), None)

        instance.set('ABC')
        self.assertEqual(instance.get(), 'ABC')

        with self.assertRaises(InvalidValueException):
            instance.set(1)

        with self.assertRaises(InvalidValueException):
            instance.set(1.5)

        instance = StringInput(default='ABC')
        self.assertEqual(instance.get(), 'ABC')

    def test_new_input(self):

        class NewInput(ValueInput):
            pass

        with self.assertRaises(NotImplementedError):
            instance = NewInput()
            instance.set(10)

        with self.assertRaises(NotImplementedError):
            instance = NewInput()
            instance.get()
