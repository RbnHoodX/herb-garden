"""Lookup herbs by common or scientific name."""

SCIENTIFIC_NAMES = {
    "basil": "Ocimum basilicum",
    "thai basil": "Ocimum basilicum var. thyrsiflora",
    "holy basil": "Ocimum tenuiflorum",
    "sweet basil": "Ocimum basilicum",
    "peppermint": "Mentha × piperita",
    "spearmint": "Mentha spicata",
    "chocolate mint": "Mentha × piperita 'Chocolate'",
    "rosemary": "Salvia rosmarinus",
    "thyme": "Thymus vulgaris",
    "lemon thyme": "Thymus citriodorus",
    "oregano": "Origanum vulgare",
    "sage": "Salvia officinalis",
    "lavender": "Lavandula angustifolia",
    "parsley": "Petroselinum crispum",
    "cilantro": "Coriandrum sativum",
    "dill": "Anethum graveolens",
    "chervil": "Anthriscus cerefolium",
    "fennel": "Foeniculum vulgare",
    "tarragon": "Artemisia dracunculus",
    "chamomile": "Matricaria chamomilla",
    "chives": "Allium schoenoprasum",
    "garlic": "Allium sativum",
    "ginger": "Zingiber officinale",
    "turmeric": "Curcuma longa",
    "bay laurel": "Laurus nobilis",
    "lemon balm": "Melissa officinalis",
    "marjoram": "Origanum majorana",
    "savory": "Satureja hortensis",
    "hyssop": "Hyssopus officinalis",
    "catnip": "Nepeta cataria",
    "echinacea": "Echinacea purpurea",
    "stevia": "Stevia rebaudiana",
    "lovage": "Levisticum officinale",
    "anise": "Pimpinella anisum",
    "cumin": "Cuminum cyminum",
    "caraway": "Carum carvi",
    "angelica": "Angelica archangelica",
    "mustard": "Sinapis alba",
    "horseradish": "Armoracia rusticana",
    "watercress": "Nasturtium officinale",
    "cardamom": "Elettaria cardamomum",
    "clove": "Syzygium aromaticum",
    "allspice": "Pimenta dioica",
}

# Reverse mapping: scientific name -> common name
_REVERSE_MAP = {}
for common, scientific in SCIENTIFIC_NAMES.items():
    if scientific not in _REVERSE_MAP:
        _REVERSE_MAP[scientific] = common


def lookup_by_common_name(name):
    """Return the scientific name for a common herb name, or None."""
    return SCIENTIFIC_NAMES.get(name.lower().strip())


def lookup_by_scientific_name(scientific):
    """Return the common name for a scientific name, or None."""
    return _REVERSE_MAP.get(scientific)


def all_common_names():
    """Return a sorted list of all known common herb names."""
    return sorted(SCIENTIFIC_NAMES.keys())


def all_scientific_names():
    """Return a sorted list of all known scientific names."""
    return sorted(set(SCIENTIFIC_NAMES.values()))


def search_names(pattern):
    """Search for herbs whose common name contains the pattern."""
    pattern_lower = pattern.lower()
    return sorted(
        name for name in SCIENTIFIC_NAMES
        if pattern_lower in name
    )


def genus_for(name):
    """Extract the genus from a herb's scientific name."""
    scientific = lookup_by_common_name(name)
    if scientific is None:
        return None
    parts = scientific.split()
    return parts[0] if parts else None


def herbs_in_genus(genus):
    """Return all common names of herbs in a given genus."""
    result = []
    for common, scientific in SCIENTIFIC_NAMES.items():
        if scientific.startswith(genus):
            result.append(common)
    return sorted(result)
