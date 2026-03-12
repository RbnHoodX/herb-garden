from config import MAX_COLLECTION_SIZE


def validate_name(name):
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    stripped = name.strip()
    if not stripped:
        raise ValueError("name cannot be empty or whitespace")
    if len(stripped) > 200:
        raise ValueError("name exceeds maximum length of 200 characters")
    return stripped


def validate_parent_id(parent_id, garden):
    if parent_id is None:
        return None
    if not isinstance(parent_id, int):
        raise TypeError("parent_id must be an integer")
    try:
        garden.get(parent_id)
    except KeyError:
        raise ValueError(f"parent herb with id {parent_id} does not exist")
    return parent_id


def is_positive_int(value):
    return isinstance(value, int) and value > 0


def sanitize_name(name):
    if not isinstance(name, str):
        return ""
    return name.strip().title()


def check_collection_size(garden):
    count = len(garden.herbs())
    if count >= MAX_COLLECTION_SIZE:
        raise ValueError(
            f"garden is full ({count}/{MAX_COLLECTION_SIZE})"
        )
    return count


def validate_herb_exists(garden, herb_id):
    try:
        return garden.get(herb_id)
    except KeyError:
        raise ValueError(f"herb with id {herb_id} does not exist")
