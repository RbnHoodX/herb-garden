def find_by_name(garden, pattern):
    pattern_lower = pattern.lower()
    return [h for h in garden.herbs() if pattern_lower in h.name.lower()]


def find_exact(garden, name):
    return [h for h in garden.herbs() if h.name == name]


def find_ancestors(herb):
    ancestors = []
    current = herb.parent
    while current is not None:
        ancestors.append(current)
        current = current.parent
    return ancestors


def find_descendants(herb):
    result = []
    stack = list(herb.children)
    while stack:
        current = stack.pop()
        result.append(current)
        stack.extend(current.children)
    return result


def depth(herb):
    d = 0
    current = herb.parent
    while current is not None:
        d += 1
        current = current.parent
    return d


def find_leaves(garden):
    return [h for h in garden.herbs() if not h.children]


def find_roots_with_children(garden):
    return [h for h in garden.roots() if h.children]


def subtree_size(herb):
    return 1 + sum(subtree_size(child) for child in herb.children)


def find_siblings(herb):
    if herb.parent is None:
        return []
    return [c for c in herb.parent.children if c.id != herb.id]
