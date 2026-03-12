import json
import csv
import sys

from config import SUPPORTED_EXPORT_FORMATS
from storage.serializer import garden_to_dict


def export_text(garden, stream=None):
    if stream is None:
        stream = sys.stdout
    herbs = garden.herbs()
    stream.write(f"Herb Garden ({len(herbs)} herbs)\n")
    stream.write("=" * 40 + "\n")
    for herb in herbs:
        parent_name = herb.parent.name if herb.parent else "-"
        child_count = len(herb.children)
        stream.write(
            f"  #{herb.id}: {herb.name} "
            f"(parent: {parent_name}, children: {child_count})\n"
        )
    stream.write("\n")


def export_csv(garden, filepath):
    herbs = garden.herbs()
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "parent_id"])
        for herb in herbs:
            parent_id = herb.parent.id if herb.parent else ""
            writer.writerow([herb.id, herb.name, parent_id])


def export_json(garden, filepath):
    data = garden_to_dict(garden)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def summary(garden):
    herbs = garden.herbs()
    roots = garden.roots()
    leaves = [h for h in herbs if not h.children]
    max_d = 0
    for herb in herbs:
        d = 0
        current = herb.parent
        while current is not None:
            d += 1
            current = current.parent
        if d > max_d:
            max_d = d
    return {
        "total": len(herbs),
        "roots": len(roots),
        "leaves": len(leaves),
        "max_depth": max_d,
    }


def validate_format(fmt):
    if fmt not in SUPPORTED_EXPORT_FORMATS:
        raise ValueError(
            f"unsupported format: {fmt}. "
            f"Supported: {', '.join(SUPPORTED_EXPORT_FORMATS)}"
        )
    return fmt
