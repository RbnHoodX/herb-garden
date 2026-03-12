import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

import pytest
from herb import Herb
from garden import Garden


class TestGardenCreation:
    def test_empty_garden(self):
        g = Garden()
        assert g.herbs() == []

    def test_create_herb(self):
        g = Garden()
        h = g.create("Basil")
        assert h.name == "Basil"
        assert h.id == 1

    def test_create_assigns_sequential_ids(self):
        g = Garden()
        a = g.create("A")
        b = g.create("B")
        c = g.create("C")
        assert a.id == 1
        assert b.id == 2
        assert c.id == 3

    def test_create_with_parent(self):
        g = Garden()
        parent = g.create("Basil")
        child = g.create("Thai Basil", parent_id=parent.id)
        assert child.parent is parent
        assert child in parent.children

    def test_create_invalid_parent_raises(self):
        g = Garden()
        with pytest.raises(KeyError):
            g.create("Orphan", parent_id=999)


class TestGardenAccess:
    def test_get_herb(self):
        g = Garden()
        h = g.create("Mint")
        assert g.get(h.id) is h

    def test_get_missing_raises(self):
        g = Garden()
        with pytest.raises(KeyError):
            g.get(999)

    def test_herbs_returns_all(self):
        g = Garden()
        g.create("A")
        g.create("B")
        g.create("C")
        assert len(g.herbs()) == 3

    def test_herbs_returns_copy(self):
        g = Garden()
        g.create("A")
        herbs = g.herbs()
        herbs.clear()
        assert len(g.herbs()) == 1


class TestGardenRoots:
    def test_roots_returns_parentless(self):
        g = Garden()
        a = g.create("A")
        b = g.create("B", parent_id=a.id)
        c = g.create("C")
        roots = g.roots()
        assert a in roots
        assert c in roots
        assert b not in roots

    def test_roots_empty_garden(self):
        g = Garden()
        assert g.roots() == []
