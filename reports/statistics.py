"""Compute statistics about the garden."""

from utils.traversal import max_depth, walk_preorder
from utils.search import find_leaves, depth


def garden_stats(garden):
    """Compute comprehensive statistics for a garden."""
    herbs = garden.herbs()
    roots = garden.roots()
    leaves = find_leaves(garden)

    stats = {
        "total_herbs": len(herbs),
        "root_count": len(roots),
        "leaf_count": len(leaves),
        "internal_count": len(herbs) - len(leaves),
        "max_depth": 0,
        "avg_depth": 0.0,
        "avg_children": 0.0,
        "max_children": 0,
        "widest_level": 0,
        "widest_level_count": 0,
    }

    if not herbs:
        return stats

    # Depth statistics
    depths = [depth(h) for h in herbs]
    stats["max_depth"] = max(depths) if depths else 0
    stats["avg_depth"] = sum(depths) / len(depths) if depths else 0.0

    # Children statistics
    children_counts = [len(h.children) for h in herbs]
    stats["max_children"] = max(children_counts) if children_counts else 0
    non_leaf_counts = [c for c in children_counts if c > 0]
    if non_leaf_counts:
        stats["avg_children"] = sum(non_leaf_counts) / len(non_leaf_counts)

    # Level width
    level_counts = {}
    for h in herbs:
        d = depth(h)
        level_counts[d] = level_counts.get(d, 0) + 1

    if level_counts:
        widest = max(level_counts, key=level_counts.get)
        stats["widest_level"] = widest
        stats["widest_level_count"] = level_counts[widest]

    return stats


def subtree_stats(herb):
    """Compute statistics for a subtree rooted at the given herb."""
    nodes = list(walk_preorder(herb))
    leaves = [n for n in nodes if not n.children]

    return {
        "size": len(nodes),
        "leaf_count": len(leaves),
        "depth": max_depth(herb),
    }


def depth_distribution(garden):
    """Return a dict mapping depth level to count of herbs at that level."""
    distribution = {}
    for herb in garden.herbs():
        d = depth(herb)
        distribution[d] = distribution.get(d, 0) + 1
    return distribution


def branching_factor(garden):
    """Compute the average branching factor for non-leaf nodes."""
    herbs = garden.herbs()
    non_leaves = [h for h in herbs if h.children]
    if not non_leaves:
        return 0.0
    total_children = sum(len(h.children) for h in non_leaves)
    return total_children / len(non_leaves)


def name_length_stats(garden):
    """Compute statistics about herb name lengths."""
    herbs = garden.herbs()
    if not herbs:
        return {"min": 0, "max": 0, "avg": 0.0, "total_chars": 0}

    lengths = [len(h.name) for h in herbs]
    return {
        "min": min(lengths),
        "max": max(lengths),
        "avg": sum(lengths) / len(lengths),
        "total_chars": sum(lengths),
    }
