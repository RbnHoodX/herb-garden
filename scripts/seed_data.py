#!/usr/bin/env python3
"""Populate a garden with sample herb data for testing."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from garden import Garden
from storage.exporter import export_json, export_text


def create_sample_garden():
    garden = Garden()

    # Lamiaceae family (mint family)
    lamiaceae = garden.create("Lamiaceae")

    mentha = garden.create("Mentha", parent_id=lamiaceae.id)
    garden.create("Peppermint", parent_id=mentha.id)
    garden.create("Spearmint", parent_id=mentha.id)
    garden.create("Chocolate Mint", parent_id=mentha.id)

    ocimum = garden.create("Ocimum", parent_id=lamiaceae.id)
    garden.create("Sweet Basil", parent_id=ocimum.id)
    garden.create("Thai Basil", parent_id=ocimum.id)
    garden.create("Holy Basil", parent_id=ocimum.id)

    garden.create("Rosemary", parent_id=lamiaceae.id)
    garden.create("Thyme", parent_id=lamiaceae.id)
    garden.create("Oregano", parent_id=lamiaceae.id)
    garden.create("Sage", parent_id=lamiaceae.id)
    garden.create("Lavender", parent_id=lamiaceae.id)

    # Apiaceae family (parsley family)
    apiaceae = garden.create("Apiaceae")
    garden.create("Parsley", parent_id=apiaceae.id)
    garden.create("Cilantro", parent_id=apiaceae.id)
    garden.create("Dill", parent_id=apiaceae.id)
    garden.create("Chervil", parent_id=apiaceae.id)
    garden.create("Fennel", parent_id=apiaceae.id)

    # Asteraceae family (daisy family)
    asteraceae = garden.create("Asteraceae")
    garden.create("Tarragon", parent_id=asteraceae.id)
    garden.create("Chamomile", parent_id=asteraceae.id)

    return garden


def main():
    garden = create_sample_garden()
    print(f"Created garden with {len(garden.herbs())} herbs")
    print(f"Root families: {len(garden.roots())}")

    if len(sys.argv) > 1:
        output = sys.argv[1]
        export_json(garden, output)
        print(f"Exported to {output}")
    else:
        export_text(garden)


if __name__ == "__main__":
    main()
