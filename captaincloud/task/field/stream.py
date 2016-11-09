from .base import Field
from .exc import InvalidValueException, StreamNotAvailableException

import six


class StreamField(Field):
    def __init__(self):
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

    def serialize(self, data):
        return data

    def deserialize(self, data):
        return data

    def validate(self, data):
        raise NotImplementedError


class StringStreamField(StreamField):
    def validate(self, data):
        if not isinstance(data, six.text_type):
            raise InvalidValueException('Expected string data')


class ByteStreamField(StreamField):
    def validate(self, data):
        if not isinstance(data, six.binary_type):
            raise InvalidValueException('Expected bytes data')
