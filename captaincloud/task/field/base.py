import copy


class Field(object):
    """Base class for fields"""

    def clone(self):
        """Clone a field"""
        return copy.deepcopy(self)

    def serialize(cls, value):
        """Serialize the input value"""
        return value

    def deserialize(cls, value):
        """Deserialize the input value"""
        return value
