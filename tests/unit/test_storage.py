import sys
import os
import json
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from herb import Herb
from garden import Garden
from storage.serializer import herb_to_dict, garden_to_dict, herb_from_dict, garden_from_dict
from storage.exporter import export_csv, export_json, summary, validate_format
from storage.loader import detect_format


class TestSerializer:
    def test_herb_to_dict(self):
        g = Garden()
        h = g.create("Basil")
        d = herb_to_dict(h)
        assert d["id"] == 1
        assert d["name"] == "Basil"
        assert d["parent_id"] is None

    def test_herb_to_dict_with_parent(self):
        g = Garden()
        a = g.create("A")
        b = g.create("B", parent_id=a.id)
        d = herb_to_dict(b)
        assert d["parent_id"] == a.id

    def test_garden_to_dict(self):
        g = Garden()
        g.create("A")
        g.create("B")
        d = garden_to_dict(g)
        assert len(d["herbs"]) == 2

    def test_herb_from_dict(self):
        h = herb_from_dict({"id": 5, "name": "Mint"})
        assert h.name == "Mint"
        assert h.id == 5

    def test_garden_roundtrip(self):
        g = Garden()
        a = g.create("Root")
        g.create("Child", parent_id=a.id)
        data = garden_to_dict(g)
        g2 = garden_from_dict(data)
        assert len(g2.herbs()) == 2
        assert len(g2.roots()) == 1


class TestExporter:
    def test_export_csv(self):
        g = Garden()
        g.create("Basil")
        g.create("Mint")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            path = f.name
        try:
            export_csv(g, path)
            with open(path) as f:
                content = f.read()
            assert "Basil" in content
            assert "Mint" in content
        finally:
            os.unlink(path)

    def test_export_json(self):
        g = Garden()
        g.create("Basil")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            path = f.name
        try:
            export_json(g, path)
            with open(path) as f:
                data = json.load(f)
            assert len(data["herbs"]) == 1
        finally:
            os.unlink(path)

    def test_summary(self):
        g = Garden()
        a = g.create("A")
        g.create("B", parent_id=a.id)
        s = summary(g)
        assert s["total"] == 2
        assert s["roots"] == 1

    def test_validate_format_valid(self):
        assert validate_format("json") == "json"

    def test_validate_format_invalid(self):
        import pytest
        with pytest.raises(ValueError):
            validate_format("xml")


class TestLoader:
    def test_detect_format_json(self):
        assert detect_format("garden.json") == "json"

    def test_detect_format_csv(self):
        assert detect_format("garden.csv") == "csv"

    def test_detect_format_unknown(self):
        assert detect_format("garden.xyz") == "unknown"
