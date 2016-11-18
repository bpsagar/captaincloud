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


class StringStreamField(StreamField):
    def create(self):
        return Stream(stream_type=six.text_type)


class ByteStreamField(StreamField):
    def create(self):
        return Stream(stream_type=six.binary_type)
