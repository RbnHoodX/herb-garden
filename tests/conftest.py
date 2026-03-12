import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from herb import Herb
from garden import Garden


@pytest.fixture
def empty_garden():
    return Garden()


@pytest.fixture
def sample_garden():
    garden = Garden()
    basil = garden.create("Basil")
    thai_basil = garden.create("Thai Basil", parent_id=basil.id)
    garden.create("Holy Basil", parent_id=basil.id)
    mint = garden.create("Mint")
    garden.create("Peppermint", parent_id=mint.id)
    garden.create("Spearmint", parent_id=mint.id)
    garden.create("Rosemary")
    return garden


@pytest.fixture
def deep_garden():
    garden = Garden()
    a = garden.create("Lamiaceae")
    b = garden.create("Mentha", parent_id=a.id)
    c = garden.create("Piperita", parent_id=b.id)
    d = garden.create("Chocolate Mint", parent_id=c.id)
    return garden
