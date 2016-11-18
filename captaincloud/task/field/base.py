import copy


class Field(object):
    """Base class for fields"""

    def serialize(cls, value):
        """Serialize the input value"""
        return value

    def deserialize(cls, value):
        """Deserialize the input value"""
        return value
