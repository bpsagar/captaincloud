"""
Field is the base class for all Task Fields
"""


class Field(object):
    """Base class for fields"""

    def serialize(cls, value):
        """Serialize the input value into serializable object"""
        return value

    def deserialize(cls, value):
        """Deserialize the input value from deserialized object"""
        return value
