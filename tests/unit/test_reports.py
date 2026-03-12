import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from garden import Garden
from reports.generator import generate_report, generate_inventory, generate_lineage
from reports.statistics import garden_stats, subtree_stats, depth_distribution, branching_factor
from reports.formatter import to_markdown, to_plain_text, format_percentage, format_bar


class TestReportGenerator:
    def test_generate_report_empty(self):
        g = Garden()
        report = generate_report(g)
        assert "Herb Garden Report" in report
        assert "Total herbs:    0" in report

    def test_generate_report_with_herbs(self):
        g = Garden()
        g.create("Basil")
        g.create("Mint")
        report = generate_report(g)
        assert "Total herbs:    2" in report
        assert "Basil" in report

    def test_generate_inventory(self):
        g = Garden()
        g.create("Basil")
        g.create("Mint")
        inv = generate_inventory(g)
        assert "Inventory: 2 herbs" in inv
        assert "Basil" in inv

    def test_generate_lineage(self):
        g = Garden()
        a = g.create("Lamiaceae")
        b = g.create("Mentha", parent_id=a.id)
        c = g.create("Peppermint", parent_id=b.id)
        lineage = generate_lineage(c)
        assert "Lamiaceae" in lineage
        assert "Mentha" in lineage
        assert "Peppermint" in lineage
        assert "→" in lineage


class TestStatistics:
    def test_empty_garden_stats(self):
        g = Garden()
        stats = garden_stats(g)
        assert stats["total_herbs"] == 0

    def test_garden_stats(self):
        g = Garden()
        a = g.create("A")
        g.create("B", parent_id=a.id)
        g.create("C", parent_id=a.id)
        stats = garden_stats(g)
        assert stats["total_herbs"] == 3
        assert stats["root_count"] == 1
        assert stats["leaf_count"] == 2

    def test_subtree_stats(self):
        g = Garden()
        a = g.create("A")
        b = g.create("B", parent_id=a.id)
        g.create("C", parent_id=b.id)
        stats = subtree_stats(a)
        assert stats["size"] == 3
        assert stats["depth"] == 2

    def test_depth_distribution(self):
        g = Garden()
        a = g.create("A")
        g.create("B", parent_id=a.id)
        dist = depth_distribution(g)
        assert dist[0] == 1
        assert dist[1] == 1

    def test_branching_factor(self):
        g = Garden()
        a = g.create("A")
        g.create("B", parent_id=a.id)
        g.create("C", parent_id=a.id)
        bf = branching_factor(g)
        assert bf == 2.0


class TestFormatter:
    def test_to_markdown(self):
        md = to_markdown("Test", [("Section", {"key": "value"})])
        assert "# Test" in md
        assert "## Section" in md
        assert "**key**" in md

    def test_to_plain_text(self):
        text = to_plain_text("Test", [("Section", "content")])
        assert "Test" in text
        assert "Section" in text

    def test_format_percentage(self):
        assert format_percentage(1, 4) == "25.0%"
        assert format_percentage(0, 0) == "0.0%"

    def test_format_bar(self):
        bar = format_bar(5, 10, width=20)
        assert len(bar) == 20
        assert "█" in bar
