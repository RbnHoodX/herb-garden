import json
import csv
import os

from storage.serializer import garden_from_dict
from garden import Garden


def load_json(filepath):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"file not found: {filepath}")
    with open(filepath, "r") as f:
        data = json.load(f)
    return garden_from_dict(data)


def load_csv(filepath):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"file not found: {filepath}")
    garden = Garden()
    with open(filepath, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name", "Unnamed")
            parent_id = row.get("parent_id", "")
            pid = int(parent_id) if parent_id else None
            garden.create(name, parent_id=pid)
    return garden


def _parse_row(row):
    return {
        "name": row.get("name", "").strip(),
        "parent_id": row.get("parent_id", "").strip() or None,
    }


def detect_format(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    format_map = {
        ".json": "json",
        ".csv": "csv",
        ".txt": "text",
    }
    return format_map.get(ext, "unknown")


def load_auto(filepath):
    fmt = detect_format(filepath)
    if fmt == "json":
        return load_json(filepath)
    elif fmt == "csv":
        return load_csv(filepath)
    else:
        raise ValueError(f"unsupported file format: {filepath}")
