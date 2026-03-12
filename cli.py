import sys

from garden import Garden
from config import Settings, VERSION
from utils.formatting import format_tree, format_table


def parse_args(argv):
    args = {"command": None, "options": {}, "positional": []}
    if not argv:
        return args
    args["command"] = argv[0]
    i = 1
    while i < len(argv):
        if argv[i].startswith("--"):
            key = argv[i].lstrip("-")
            if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
                args["options"][key] = argv[i + 1]
                i += 2
            else:
                args["options"][key] = True
                i += 1
        else:
            args["positional"].append(argv[i])
            i += 1
    return args


def format_help():
    lines = [
        f"herb-garden v{VERSION}",
        "",
        "Usage: herb-garden <command> [options]",
        "",
        "Commands:",
        "  list              List all herbs in the garden",
        "  add <name>        Add a new herb to the garden",
        "  tree              Display the herb hierarchy as a tree",
        "  info <id>         Show details for a specific herb",
        "  search <pattern>  Search herbs by name",
        "  export            Export the garden to a file",
        "  stats             Show garden statistics",
        "  help              Show this help message",
        "",
        "Options:",
        "  --parent <id>     Specify parent herb for add command",
        "  --format <fmt>    Export format: text, csv, json (default: text)",
        "  --no-ids          Hide herb IDs in output",
        "  --output <file>   Output file path for export",
    ]
    return "\n".join(lines)


def run(command, garden, options=None, positional=None):
    if options is None:
        options = {}
    if positional is None:
        positional = []
    if command == "list":
        herbs = garden.herbs()
        if not herbs:
            print("No herbs in the garden.")
            return 0
        show_ids = not options.get("no-ids", False)
        print(format_table(herbs, show_ids=show_ids))
        return len(herbs)
    elif command == "add":
        name = positional[0] if positional else options.get("name", "Unnamed")
        parent_id = options.get("parent")
        if parent_id is not None:
            parent_id = int(parent_id)
        herb = garden.create(name, parent_id=parent_id)
        print(f"Added: {herb}")
        return herb
    elif command == "tree":
        roots = garden.roots()
        if not roots:
            print("Garden is empty.")
            return 0
        show_ids = not options.get("no-ids", False)
        print(format_tree(garden, show_ids=show_ids))
        return len(roots)
    elif command == "info":
        herb_id = int(positional[0]) if positional else None
        if herb_id is None:
            print("Error: provide a herb ID")
            return None
        try:
            herb = garden.get(herb_id)
        except KeyError:
            print(f"Error: herb #{herb_id} not found")
            return None
        print(f"ID:       {herb.id}")
        print(f"Name:     {herb.name}")
        parent_name = herb.parent.name if herb.parent else "(none)"
        print(f"Parent:   {parent_name}")
        print(f"Children: {len(herb.children)}")
        return herb
    elif command == "search":
        pattern = positional[0] if positional else ""
        from utils.search import find_by_name
        results = find_by_name(garden, pattern)
        if not results:
            print(f"No herbs matching '{pattern}'")
            return []
        for h in results:
            print(f"  #{h.id}: {h.name}")
        return results
    elif command == "stats":
        from storage.exporter import summary
        s = summary(garden)
        print(f"Total herbs: {s['total']}")
        print(f"Root herbs:  {s['roots']}")
        print(f"Max depth:   {s['max_depth']}")
        return s
    elif command == "export":
        fmt = options.get("format", "text")
        output = options.get("output")
        from storage.exporter import export_text, export_csv, export_json
        if fmt == "csv" and output:
            export_csv(garden, output)
            print(f"Exported to {output}")
        elif fmt == "json" and output:
            export_json(garden, output)
            print(f"Exported to {output}")
        else:
            export_text(garden)
        return True
    elif command == "help":
        print(format_help())
        return True
    else:
        print(f"Unknown command: {command}")
        print("Run 'herb-garden help' for usage information.")
        return None


def main():
    args = parse_args(sys.argv[1:])
    garden = Garden()
    if args["command"] is None:
        print(format_help())
        return
    run(args["command"], garden, args["options"], args["positional"])


if __name__ == "__main__":
    main()
