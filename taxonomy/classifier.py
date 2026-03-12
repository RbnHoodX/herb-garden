"""Classify herbs into botanical families and categories."""

HERB_FAMILIES = {
    "Lamiaceae": {
        "common_name": "Mint family",
        "members": [
            "basil", "mint", "rosemary", "thyme", "oregano", "sage",
            "lavender", "marjoram", "savory", "peppermint", "spearmint",
            "lemon balm", "catnip", "hyssop", "perilla",
        ],
    },
    "Apiaceae": {
        "common_name": "Parsley family",
        "members": [
            "parsley", "cilantro", "dill", "chervil", "fennel",
            "cumin", "caraway", "anise", "lovage", "angelica",
        ],
    },
    "Asteraceae": {
        "common_name": "Daisy family",
        "members": [
            "tarragon", "chamomile", "echinacea", "stevia",
            "chicory", "dandelion", "artichoke",
        ],
    },
    "Amaryllidaceae": {
        "common_name": "Onion family",
        "members": [
            "chives", "garlic", "leek", "shallot", "ramps",
        ],
    },
    "Zingiberaceae": {
        "common_name": "Ginger family",
        "members": [
            "ginger", "turmeric", "cardamom", "galangal",
        ],
    },
    "Lauraceae": {
        "common_name": "Laurel family",
        "members": [
            "bay laurel", "bay leaf", "cinnamon", "sassafras",
        ],
    },
    "Brassicaceae": {
        "common_name": "Mustard family",
        "members": [
            "mustard", "horseradish", "wasabi", "watercress", "arugula",
        ],
    },
    "Myrtaceae": {
        "common_name": "Myrtle family",
        "members": [
            "clove", "allspice", "eucalyptus", "myrtle",
        ],
    },
}

GROWTH_TYPES = {
    "annual": [
        "basil", "cilantro", "dill", "chervil", "cumin",
        "anise", "chamomile", "stevia", "parsley",
    ],
    "perennial": [
        "mint", "rosemary", "thyme", "oregano", "sage",
        "lavender", "tarragon", "chives", "fennel", "lemon balm",
        "marjoram", "hyssop", "lovage", "echinacea",
    ],
    "biennial": [
        "parsley", "caraway", "angelica",
    ],
}

CULINARY_USES = {
    "savory": [
        "basil", "rosemary", "thyme", "oregano", "sage", "parsley",
        "cilantro", "dill", "chives", "tarragon", "marjoram", "savory",
    ],
    "sweet": [
        "mint", "lavender", "stevia", "chamomile", "lemon balm",
        "vanilla", "cinnamon",
    ],
    "medicinal": [
        "chamomile", "echinacea", "ginger", "turmeric", "lavender",
        "peppermint", "lemon balm", "valerian", "garlic",
    ],
    "aromatic": [
        "lavender", "rosemary", "mint", "basil", "thyme",
        "lemon balm", "sage",
    ],
}


def classify_herb(name):
    """Return classification info for a herb by common name."""
    name_lower = name.lower().strip()
    result = {
        "name": name,
        "family": None,
        "family_common_name": None,
        "growth_type": None,
        "culinary_uses": [],
    }

    for family, info in HERB_FAMILIES.items():
        if name_lower in info["members"]:
            result["family"] = family
            result["family_common_name"] = info["common_name"]
            break

    for growth_type, members in GROWTH_TYPES.items():
        if name_lower in members:
            result["growth_type"] = growth_type
            break

    for use_type, members in CULINARY_USES.items():
        if name_lower in members:
            result["culinary_uses"].append(use_type)

    return result


def get_family(name):
    """Return the botanical family name for a herb, or None."""
    name_lower = name.lower().strip()
    for family, info in HERB_FAMILIES.items():
        if name_lower in info["members"]:
            return family
    return None


def list_families():
    """Return a sorted list of all botanical family names."""
    return sorted(HERB_FAMILIES.keys())


def family_members(family):
    """Return the list of herb names in a given family."""
    info = HERB_FAMILIES.get(family)
    if info is None:
        return []
    return list(info["members"])


def is_perennial(name):
    """Check if a herb is perennial."""
    return name.lower().strip() in GROWTH_TYPES.get("perennial", [])


def is_annual(name):
    """Check if a herb is annual."""
    return name.lower().strip() in GROWTH_TYPES.get("annual", [])


def culinary_uses_for(name):
    """Return the list of culinary use categories for a herb."""
    name_lower = name.lower().strip()
    uses = []
    for use_type, members in CULINARY_USES.items():
        if name_lower in members:
            uses.append(use_type)
    return uses
