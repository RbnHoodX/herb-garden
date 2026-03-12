import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from taxonomy.classifier import classify_herb, get_family, list_families, is_perennial, is_annual
from taxonomy.lookup import lookup_by_common_name, lookup_by_scientific_name, search_names, genus_for
from taxonomy.companions import get_good_companions, get_bad_companions, are_compatible


class TestClassifier:
    def test_classify_basil(self):
        info = classify_herb("basil")
        assert info["family"] == "Lamiaceae"
        assert info["family_common_name"] == "Mint family"
        assert "savory" in info["culinary_uses"]

    def test_classify_unknown(self):
        info = classify_herb("unknown_plant")
        assert info["family"] is None

    def test_get_family_rosemary(self):
        assert get_family("rosemary") == "Lamiaceae"

    def test_get_family_parsley(self):
        assert get_family("parsley") == "Apiaceae"

    def test_get_family_unknown(self):
        assert get_family("xyz") is None

    def test_list_families(self):
        families = list_families()
        assert "Lamiaceae" in families
        assert "Apiaceae" in families
        assert families == sorted(families)

    def test_is_perennial(self):
        assert is_perennial("rosemary") is True
        assert is_perennial("basil") is False

    def test_is_annual(self):
        assert is_annual("basil") is True
        assert is_annual("rosemary") is False


class TestLookup:
    def test_lookup_common(self):
        result = lookup_by_common_name("basil")
        assert result == "Ocimum basilicum"

    def test_lookup_common_case_insensitive(self):
        result = lookup_by_common_name("BASIL")
        assert result == "Ocimum basilicum"

    def test_lookup_scientific(self):
        result = lookup_by_scientific_name("Ocimum basilicum")
        assert result is not None

    def test_lookup_unknown(self):
        assert lookup_by_common_name("martian herb") is None

    def test_search_names(self):
        results = search_names("mint")
        assert "peppermint" in results
        assert "spearmint" in results

    def test_genus_for(self):
        assert genus_for("basil") == "Ocimum"
        assert genus_for("rosemary") == "Salvia"


class TestCompanions:
    def test_good_companions_basil(self):
        companions = get_good_companions("basil")
        assert "tomato" in companions

    def test_bad_companions_basil(self):
        bad = get_bad_companions("basil")
        assert "sage" in bad

    def test_compatible(self):
        assert are_compatible("basil", "tomato") is True

    def test_incompatible(self):
        assert are_compatible("basil", "sage") is False

    def test_unknown_herb_compatible(self):
        assert are_compatible("xyz", "abc") is True
