import sys
import os
import json
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from garden import Garden
from storage.serializer import garden_to_dict, garden_from_dict
from storage.exporter import export_json, summary
from storage.loader import load_json
from reports.generator import generate_report, generate_inventory
from reports.statistics import garden_stats
from taxonomy.classifier import classify_herb, get_family
from taxonomy.lookup import lookup_by_common_name
from taxonomy.companions import are_compatible
from utils.traversal import collect_subtree, max_depth
from utils.search import find_by_name, find_leaves


class TestEndToEnd:
    def test_create_export_reload(self):
        g = Garden()
        a = g.create("Lamiaceae")
        g.create("Basil", parent_id=a.id)
        g.create("Mint", parent_id=a.id)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            path = f.name
        try:
            export_json(g, path)
            g2 = load_json(path)
            assert len(g2.herbs()) == 3
            assert len(g2.roots()) == 1
        finally:
            os.unlink(path)

    def test_report_with_taxonomy(self):
        g = Garden()
        g.create("Basil")
        g.create("Rosemary")
        g.create("Parsley")

        report = generate_report(g)
        assert "Total herbs:    3" in report

        for herb in g.herbs():
            info = classify_herb(herb.name)
            assert info["name"] == herb.name

    def test_stats_and_search(self):
        g = Garden()
        a = g.create("Mint Family")
        g.create("Peppermint", parent_id=a.id)
        g.create("Spearmint", parent_id=a.id)
        g.create("Chocolate Mint", parent_id=a.id)

        stats = garden_stats(g)
        assert stats["total_herbs"] == 4
        assert stats["leaf_count"] == 3

        results = find_by_name(g, "mint")
        assert len(results) >= 3

    def test_taxonomy_integration(self):
        assert get_family("basil") == "Lamiaceae"
        assert get_family("parsley") == "Apiaceae"
        assert lookup_by_common_name("rosemary") is not None
        assert are_compatible("basil", "oregano") is True

    def test_traversal_with_report(self):
        g = Garden()
        a = g.create("Root")
        b = g.create("L1", parent_id=a.id)
        c = g.create("L2", parent_id=b.id)
        d = g.create("L3", parent_id=c.id)

        subtree = collect_subtree(a)
        assert len(subtree) == 4
        assert max_depth(a) == 3

        inventory = generate_inventory(g)
        assert "Root" in inventory
        assert "L3" in inventory

    def test_full_garden_workflow(self):
        g = Garden()

        # Build a realistic garden
        lamiaceae = g.create("Lamiaceae")
        apiaceae = g.create("Apiaceae")

        basil = g.create("Basil", parent_id=lamiaceae.id)
        g.create("Thai Basil", parent_id=basil.id)
        g.create("Holy Basil", parent_id=basil.id)

        mint = g.create("Mint", parent_id=lamiaceae.id)
        g.create("Peppermint", parent_id=mint.id)
        g.create("Spearmint", parent_id=mint.id)

        g.create("Rosemary", parent_id=lamiaceae.id)
        g.create("Thyme", parent_id=lamiaceae.id)

        g.create("Parsley", parent_id=apiaceae.id)
        g.create("Cilantro", parent_id=apiaceae.id)
        g.create("Dill", parent_id=apiaceae.id)

        # Verify structure
        assert len(g.herbs()) == 13
        assert len(g.roots()) == 2
        assert len(find_leaves(g)) == 9

        # Verify stats
        stats = garden_stats(g)
        assert stats["total_herbs"] == 13
        assert stats["max_depth"] == 2

        # Verify serialization roundtrip
        data = garden_to_dict(g)
        g2 = garden_from_dict(data)
        assert len(g2.herbs()) == 13

        # Verify report generation
        report = generate_report(g)
        assert "13" in report
