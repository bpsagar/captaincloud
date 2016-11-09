import copy


class Field(object):
    """Base class for fields"""

    def clone(self):
        """Clone a field"""
        return copy.deepcopy(self)

    @classmethod
    def serialize(cls, value):
        """Serialize the input value"""
        return value

    @classmethod
    def deserialize(cls, value):
        """Deserialize the input value"""
        return value
