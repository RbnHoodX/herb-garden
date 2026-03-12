"""Format report data into various output styles."""

import csv
import io
import json


def to_markdown(title, sections):
    """Format report sections as Markdown.

    Args:
        title: Report title string.
        sections: List of (heading, content) tuples.
    """
    lines = [f"# {title}", ""]
    for heading, content in sections:
        lines.append(f"## {heading}")
        lines.append("")
        if isinstance(content, dict):
            for key, value in content.items():
                lines.append(f"- **{key}**: {value}")
        elif isinstance(content, list):
            for item in content:
                lines.append(f"- {item}")
        else:
            lines.append(str(content))
        lines.append("")
    return "\n".join(lines)


def to_csv_string(headers, rows):
    """Format tabular data as a CSV string."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
    return buf.getvalue()


def to_json_string(data, indent=2):
    """Format data as a pretty-printed JSON string."""
    return json.dumps(data, indent=indent, default=str)


def to_plain_text(title, sections):
    """Format report sections as plain text."""
    lines = [title, "=" * len(title), ""]
    for heading, content in sections:
        lines.append(heading)
        lines.append("-" * len(heading))
        if isinstance(content, dict):
            for key, value in content.items():
                lines.append(f"  {key}: {value}")
        elif isinstance(content, list):
            for item in content:
                lines.append(f"  - {item}")
        else:
            lines.append(f"  {content}")
        lines.append("")
    return "\n".join(lines)


def format_number(value, decimals=2):
    """Format a number with the specified decimal places."""
    if isinstance(value, float):
        return f"{value:.{decimals}f}"
    return str(value)


def format_percentage(part, whole):
    """Format a fraction as a percentage string."""
    if whole == 0:
        return "0.0%"
    pct = (part / whole) * 100
    return f"{pct:.1f}%"


def format_bar(value, max_value, width=40, char="█"):
    """Create a simple text bar chart element."""
    if max_value == 0:
        return ""
    filled = int((value / max_value) * width)
    return char * filled + "░" * (width - filled)


def format_table_row(values, widths):
    """Format a single table row with column widths."""
    parts = []
    for value, width in zip(values, widths):
        parts.append(str(value).ljust(width))
    return " | ".join(parts)
