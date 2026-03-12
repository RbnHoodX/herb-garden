from collections import deque


def walk_preorder(herb):
    yield herb
    for child in herb.children:
        yield from walk_preorder(child)


def walk_postorder(herb):
    for child in herb.children:
        yield from walk_postorder(child)
    yield herb


def walk_breadth_first(herb):
    queue = deque([herb])
    while queue:
        current = queue.popleft()
        yield current
        queue.extend(current.children)


def collect_subtree(herb):
    return list(walk_preorder(herb))


def max_depth(herb):
    if not herb.children:
        return 0
    return 1 + max(max_depth(c) for c in herb.children)


def path_to_root(herb):
    path = []
    current = herb
    while current is not None:
        path.append(current)
        current = current.parent
    return path


def common_ancestor(herb_a, herb_b):
    path_a = set()
    current = herb_a
    while current is not None:
        path_a.add(current.id)
        current = current.parent
    current = herb_b
    while current is not None:
        if current.id in path_a:
            return current
        current = current.parent
    return None


def level_order(garden):
    result = {}
    for herb in garden.herbs():
        d = 0
        current = herb.parent
        while current is not None:
            d += 1
            current = current.parent
        if d not in result:
            result[d] = []
        result[d].append(herb)
    return result
