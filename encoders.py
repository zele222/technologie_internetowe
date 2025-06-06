from sqlalchemy.orm import class_mapper

def to_dict(obj):
    """Convert SQLAlchemy model instance to dictionary, excluding problematic geometry fields."""
    if not obj:
        return None

    excluded_fields = {"position"}  # 👈 pola do pominięcia

    result = {}
    for column in class_mapper(obj.__class__).columns:
        if column.key not in excluded_fields:
            try:
                result[column.key] = getattr(obj, column.key)
            except Exception:
                result[column.key] = None  # lub pominąć całkowicie
    return result
