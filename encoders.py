from sqlalchemy.orm import class_mapper

def to_dict(obj):
    """Prosta konwersja SQLAlchemy obiektu do dict bez pól Geometry."""
    if not obj:
        return None
    return {
        column.key: getattr(obj, column.key)
        for column in class_mapper(obj.__class__).columns
        if column.key != "position"  # zakładamy, że chcesz pominąć to pole
    }
