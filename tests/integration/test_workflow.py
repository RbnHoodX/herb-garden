import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from herb import Herb
from garden import Garden
from utils.search import find_by_name, find_leaves
from utils.traversal import collect_subtree, max_depth


class TestFullWorkflow:
    def test_build_herb_family(self):
        g = Garden()
        lamiaceae = g.create("Lamiaceae")
        mentha = g.create("Mentha", parent_id=lamiaceae.id)
        ocimum = g.create("Ocimum", parent_id=lamiaceae.id)
        g.create("Peppermint", parent_id=mentha.id)
        g.create("Spearmint", parent_id=mentha.id)
        g.create("Sweet Basil", parent_id=ocimum.id)

        assert len(g.herbs()) == 6
        assert len(g.roots()) == 1
        assert len(find_leaves(g)) == 3
        assert max_depth(lamiaceae) == 2

    def test_multiple_root_families(self):
        g = Garden()
        lamiaceae = g.create("Lamiaceae")
        apiaceae = g.create("Apiaceae")
        g.create("Basil", parent_id=lamiaceae.id)
        g.create("Mint", parent_id=lamiaceae.id)
        g.create("Parsley", parent_id=apiaceae.id)
        g.create("Cilantro", parent_id=apiaceae.id)

        assert len(g.roots()) == 2
        assert len(g.herbs()) == 6

    def test_search_across_tree(self):
        g = Garden()
        a = g.create("Basil")
        g.create("Thai Basil", parent_id=a.id)
        g.create("Holy Basil", parent_id=a.id)
        g.create("Mint")

        results = find_by_name(g, "Basil")
        assert len(results) == 3

    def test_subtree_collection(self):
        g = Garden()
        a = g.create("Root")
        b = g.create("Child1", parent_id=a.id)
        c = g.create("Child2", parent_id=a.id)
        d = g.create("Grandchild", parent_id=b.id)

        subtree = collect_subtree(a)
        assert len(subtree) == 4
        assert subtree[0] is a

    def test_herb_repr_stability(self):
        g = Garden()
        h = g.create("Oregano")
        assert repr(h) == "Herb(id=1, name='Oregano')"
