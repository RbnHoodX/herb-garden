def format_herb(herb, show_id=True):
    if show_id:
        return f"#{herb.id}: {herb.name}"
    return herb.name


def format_tree(garden, root_id=None, show_ids=True):
    lines = []
    if root_id is not None:
        root = garden.get(root_id)
        _build_tree_lines(root, lines, "", True, show_ids)
    else:
        roots = garden.roots()
        for i, root in enumerate(roots):
            _build_tree_lines(root, lines, "", i == len(roots) - 1, show_ids)
    return "\n".join(lines)


def _build_tree_lines(herb, lines, prefix, is_last, show_ids):
    connector = "└── " if is_last else "├── "
    label = f"{herb.name} (#{herb.id})" if show_ids else herb.name
    lines.append(f"{prefix}{connector}{label}")
    children = herb.children
    for i, child in enumerate(children):
        extension = "    " if is_last else "│   "
        _build_tree_lines(child, lines, prefix + extension, i == len(children) - 1, show_ids)


def format_table(herbs, columns=None, show_ids=True):
    if not herbs:
        return "(empty)"
    rows = []
    if show_ids:
        header = f"{'ID':>4}  {'NAME':<30}"
        rows.append(header)
        rows.append("-" * len(header))
        for herb in herbs:
            rows.append(f"{herb.id:>4}  {herb.name:<30}")
    else:
        header = f"{'NAME':<30}"
        rows.append(header)
        rows.append("-" * len(header))
        for herb in herbs:
            rows.append(f"{herb.name:<30}")
    return "\n".join(rows)


def truncate(text, max_length=40):
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def indent_lines(text, level=1, width=2):
    prefix = " " * (level * width)
    return "\n".join(prefix + line for line in text.splitlines())
