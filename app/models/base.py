from sqlalchemy.inspection import inspect

class BaseRepo:
    @classmethod
    def to_dict(cls, obj):
        if obj is None:
            return None
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
