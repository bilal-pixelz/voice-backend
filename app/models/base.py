import enum
from sqlalchemy.inspection import inspect

class BaseRepo:
    @classmethod
    def to_dict(cls, obj):
        if obj is None:
            return None
        d = {}
        for c in inspect(obj).mapper.column_attrs:
            val = getattr(obj, c.key)
            if isinstance(val, enum.Enum):
                d[c.key] = val.value
            else:
                d[c.key] = val
        return d
