import copy


class Field(object):
    """Base class for fields"""

    def clone(self):
        """Clone a field"""
        return copy.deepcopy(self)
