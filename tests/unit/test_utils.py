import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from herb import Herb
from garden import Garden
from utils.search import find_by_name, find_ancestors, find_descendants, depth, find_leaves
from utils.validation import validate_name, sanitize_name, is_positive_int
from utils.traversal import walk_preorder, walk_postorder, collect_subtree, max_depth
from utils.formatting import format_herb, truncate


class TestSearch:
    def test_find_by_name(self):
        g = Garden()
        g.create("Basil")
        g.create("Thai Basil")
        g.create("Mint")
        results = find_by_name(g, "basil")
        assert len(results) == 2

    def test_find_ancestors(self):
        g = Garden()
        a = g.create("A")
        b = g.create("B", parent_id=a.id)
        c = g.create("C", parent_id=b.id)
        ancestors = find_ancestors(c)
        assert len(ancestors) == 2
        assert ancestors[0] is b
        assert ancestors[1] is a

    def test_find_descendants(self):
        g = Garden()
        a = g.create("A")
        b = g.create("B", parent_id=a.id)
        c = g.create("C", parent_id=a.id)
        desc = find_descendants(a)
        assert len(desc) == 2

    def test_depth(self):
        g = Garden()
        a = g.create("A")
        b = g.create("B", parent_id=a.id)
        c = g.create("C", parent_id=b.id)
        assert depth(a) == 0
        assert depth(b) == 1
        assert depth(c) == 2

    def test_find_leaves(self):
        g = Garden()
        a = g.create("A")
        g.create("B", parent_id=a.id)
        g.create("C", parent_id=a.id)
        leaves = find_leaves(g)
        assert len(leaves) == 2


class TestValidation:
    def test_validate_name_valid(self):
        assert validate_name("Basil") == "Basil"

    def test_validate_name_strips(self):
        assert validate_name("  Basil  ") == "Basil"

    def test_validate_name_empty_raises(self):
        import pytest
        with pytest.raises(ValueError):
            validate_name("")

    def test_sanitize_name(self):
        assert sanitize_name("thai basil") == "Thai Basil"

    def test_is_positive_int(self):
        assert is_positive_int(1) is True
        assert is_positive_int(0) is False
        assert is_positive_int(-1) is False
        assert is_positive_int("1") is False


class TestTraversal:
    def test_walk_preorder(self):
        g = Garden()
        a = g.create("A")
        b = g.create("B", parent_id=a.id)
        c = g.create("C", parent_id=a.id)
        order = list(walk_preorder(a))
        assert order[0] is a
        assert len(order) == 3

    def test_walk_postorder(self):
        g = Garden()
        a = g.create("A")
        b = g.create("B", parent_id=a.id)
        order = list(walk_postorder(a))
        assert order[-1] is a
        assert order[0] is b

    def test_collect_subtree(self):
        g = Garden()
        a = g.create("A")
        b = g.create("B", parent_id=a.id)
        subtree = collect_subtree(a)
        assert len(subtree) == 2

    def test_max_depth_leaf(self):
        h = Herb("leaf")
        assert max_depth(h) == 0

    def test_max_depth_tree(self):
        g = Garden()
        a = g.create("A")
        b = g.create("B", parent_id=a.id)
        c = g.create("C", parent_id=b.id)
        assert max_depth(a) == 2


class TestFormatting:
    def test_format_herb_with_id(self):
        h = Herb("Basil")
        h.id = 1
        assert format_herb(h) == "#1: Basil"

    def test_format_herb_without_id(self):
        h = Herb("Basil")
        assert format_herb(h, show_id=False) == "Basil"

    def test_truncate_short(self):
        assert truncate("hi", 10) == "hi"

    def test_truncate_long(self):
        assert truncate("a" * 50, 10) == "aaaaaaa..."
