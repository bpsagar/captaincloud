from .base import Field
from .exc import InvalidValueException, StreamNotAvailableException

import six


class Stream(object):
    def __init__(self, stream_type):
        self.stream_type = stream_type
        self.real_stream = None

    def set_real_stream(self, real_stream):
        self.real_stream = real_stream

    def read(self, n=-1):
        if self.real_stream is None:
            raise StreamNotAvailableException()
        return self.deserialize(self.real_stream.read(n))

    def write(self, data=None):
        if self.real_stream is None:
            raise StreamNotAvailableException()
        self.validate(data)
        return self.real_stream.write(self.serialize(data))

    def close(self):
        if self.real_stream is None:
            raise StreamNotAvailableException()
        self.real_stream.close()

    def validate(self, data):
        if not isinstance(data, self.stream_type):
            raise InvalidValueException()

    def serialize(self, data):
        return data

    def deserialize(self, data):
        return data


class StreamField(Field):
    def create(self):
        raise NotImplementedError

    def get_initial(self):
        return self.create()

    @classmethod
    def is_serializable(cls):
        return False

    @classmethod
    def make_property(cls, name):
        """Returns a property function for a field"""

        def _get(self):
            return self.__values__[name]

        def _set(self, value):
            self.__values__[name].set_real_stream(value)

        return property(fget=_get, fset=_set)


class StringStreamField(StreamField):
    def create(self):
        return Stream(stream_type=six.text_type)


class ByteStreamField(StreamField):
    def create(self):
        return Stream(stream_type=six.binary_type)
