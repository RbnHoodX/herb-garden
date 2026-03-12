import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from herb import Herb


class TestHerbCreation:
    def test_default_name(self):
        h = Herb()
        assert h.name == ""

    def test_custom_name(self):
        h = Herb(name="Basil")
        assert h.name == "Basil"

    def test_default_id(self):
        h = Herb()
        assert h.id == 0

    def test_id_setter(self):
        h = Herb()
        h.id = 42
        assert h.id == 42

    def test_default_parent(self):
        h = Herb()
        assert h.parent is None

    def test_default_children(self):
        h = Herb()
        assert h.children == []

    def test_children_returns_copy(self):
        h = Herb()
        children = h.children
        children.append("fake")
        assert h.children == []


class TestHerbRepr:
    def test_repr_default(self):
        h = Herb()
        assert repr(h) == "Herb(id=0, name='')"

    def test_repr_with_name(self):
        h = Herb(name="Thyme")
        assert repr(h) == "Herb(id=0, name='Thyme')"

    def test_repr_with_id(self):
        h = Herb(name="Sage")
        h.id = 5
        assert repr(h) == "Herb(id=5, name='Sage')"


class TestHerbRegistry:
    def test_registry_exists(self):
        assert hasattr(Herb, "_registry")
        assert isinstance(Herb._registry, dict)

    def test_subclass_registered(self):
        class TestVariety(Herb):
            pass
        assert "TestVariety" in Herb._registry

    def test_fields_attribute(self):
        assert hasattr(Herb, "_fields")
        assert "name" in Herb._fields
