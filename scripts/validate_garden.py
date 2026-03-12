#!/usr/bin/env python3
"""Validate the integrity of a garden's hierarchy."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from garden import Garden
from utils.traversal import walk_preorder, max_depth
from utils.search import find_leaves


def validate_garden(garden):
    errors = []
    herbs = garden.herbs()

    # Check for duplicate IDs
    seen_ids = set()
    for herb in herbs:
        if herb.id in seen_ids:
            errors.append(f"Duplicate ID: {herb.id}")
        seen_ids.add(herb.id)

    # Check parent-child consistency
    for herb in herbs:
        if herb.parent is not None:
            if herb not in herb.parent.children:
                errors.append(
                    f"Herb #{herb.id} ({herb.name}) has parent "
                    f"#{herb.parent.id} but is not in parent's children"
                )

    for herb in herbs:
        for child in herb.children:
            if child.parent is not herb:
                errors.append(
                    f"Herb #{herb.id} ({herb.name}) lists "
                    f"#{child.id} as child but child's parent differs"
                )

    # Check for cycles
    for herb in herbs:
        visited = set()
        current = herb
        while current is not None:
            if current.id in visited:
                errors.append(f"Cycle detected involving herb #{herb.id}")
                break
            visited.add(current.id)
            current = current.parent

    return errors


def print_report(garden):
    errors = validate_garden(garden)
    herbs = garden.herbs()
    roots = garden.roots()
    leaves = find_leaves(garden)

    print("Garden Validation Report")
    print("=" * 40)
    print(f"Total herbs:  {len(herbs)}")
    print(f"Root herbs:   {len(roots)}")
    print(f"Leaf herbs:   {len(leaves)}")

    if roots:
        depths = [max_depth(r) for r in roots]
        print(f"Max depth:    {max(depths)}")

    if errors:
        print(f"\nErrors found: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\nNo errors found. Garden is valid.")


if __name__ == "__main__":
    garden = Garden()
    print_report(garden)
