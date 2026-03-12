"""Generate formatted reports from garden data."""
import io
from datetime import datetime

from utils.traversal import walk_preorder, max_depth
from utils.search import find_leaves, depth


def generate_report(garden, title=None, include_tree=True, include_stats=True):
    """Generate a comprehensive garden report as a string."""
    buf = io.StringIO()

    if title is None:
        title = "Herb Garden Report"

    buf.write(f"{title}\n")
    buf.write("=" * len(title) + "\n")
    buf.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

    herbs = garden.herbs()
    roots = garden.roots()
    leaves = find_leaves(garden)

    if include_stats:
        buf.write("Summary\n")
        buf.write("-" * 30 + "\n")
        buf.write(f"  Total herbs:    {len(herbs)}\n")
        buf.write(f"  Root families:  {len(roots)}\n")
        buf.write(f"  Leaf varieties: {len(leaves)}\n")
        if roots:
            max_d = max(max_depth(r) for r in roots)
            buf.write(f"  Maximum depth:  {max_d}\n")
        buf.write("\n")

    if include_tree and roots:
        buf.write("Hierarchy\n")
        buf.write("-" * 30 + "\n")
        for root in roots:
            _write_tree(buf, root, "", True)
        buf.write("\n")

    if herbs:
        buf.write("Herb Index\n")
        buf.write("-" * 30 + "\n")
        for herb in sorted(herbs, key=lambda h: h.name.lower()):
            d = depth(herb)
            parent_info = f" (under {herb.parent.name})" if herb.parent else ""
            buf.write(f"  #{herb.id}: {herb.name}{parent_info} [depth={d}]\n")

    return buf.getvalue()


def _write_tree(buf, herb, prefix, is_last):
    connector = "└── " if is_last else "├── "
    buf.write(f"{prefix}{connector}{herb.name} (#{herb.id})\n")
    children = herb.children
    for i, child in enumerate(children):
        extension = "    " if is_last else "│   "
        _write_tree(buf, child, prefix + extension, i == len(children) - 1)


def generate_inventory(garden):
    """Generate a simple inventory listing."""
    lines = []
    herbs = garden.herbs()
    lines.append(f"Inventory: {len(herbs)} herbs")
    lines.append("")
    for herb in sorted(herbs, key=lambda h: h.id):
        children_count = len(herb.children)
        parent_name = herb.parent.name if herb.parent else "—"
        lines.append(
            f"  [{herb.id:04d}] {herb.name:<30} "
            f"parent={parent_name:<20} children={children_count}"
        )
    return "\n".join(lines)


def generate_lineage(herb):
    """Generate the lineage path from root to a specific herb."""
    path = []
    current = herb
    while current is not None:
        path.append(current)
        current = current.parent
    path.reverse()
    parts = [f"{h.name} (#{h.id})" for h in path]
    return " → ".join(parts)


def generate_comparison(garden_a, garden_b):
    """Compare two gardens and report differences."""
    names_a = {h.name for h in garden_a.herbs()}
    names_b = {h.name for h in garden_b.herbs()}

    only_a = sorted(names_a - names_b)
    only_b = sorted(names_b - names_a)
    common = sorted(names_a & names_b)

    lines = [
        f"Garden A: {len(names_a)} herbs",
        f"Garden B: {len(names_b)} herbs",
        f"Common:   {len(common)} herbs",
        "",
    ]

    if only_a:
        lines.append("Only in Garden A:")
        for name in only_a:
            lines.append(f"  - {name}")
        lines.append("")

    if only_b:
        lines.append("Only in Garden B:")
        for name in only_b:
            lines.append(f"  - {name}")
        lines.append("")

    if common:
        lines.append("In both gardens:")
        for name in common:
            lines.append(f"  * {name}")

    return "\n".join(lines)
