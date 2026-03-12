"""Companion planting relationships for herbs."""

GOOD_COMPANIONS = {
    "basil": ["tomato", "pepper", "oregano", "parsley", "chamomile"],
    "mint": ["cabbage", "tomato", "pea"],
    "rosemary": ["sage", "thyme", "lavender", "bean", "carrot", "cabbage"],
    "thyme": ["rosemary", "lavender", "eggplant", "tomato", "strawberry"],
    "oregano": ["basil", "pepper", "tomato", "grape"],
    "sage": ["rosemary", "cabbage", "carrot", "strawberry", "tomato"],
    "lavender": ["rosemary", "thyme", "sage", "chamomile"],
    "parsley": ["basil", "tomato", "asparagus", "corn", "rose"],
    "cilantro": ["spinach", "pea", "tomato", "anise"],
    "dill": ["cabbage", "lettuce", "onion", "cucumber"],
    "chives": ["carrot", "tomato", "parsley", "rose", "grape"],
    "tarragon": ["eggplant", "pepper", "tomato"],
    "chamomile": ["basil", "cabbage", "onion", "cucumber", "mint"],
    "fennel": [],
    "marjoram": ["sage", "thyme", "basil", "oregano"],
}

BAD_COMPANIONS = {
    "basil": ["sage", "rue"],
    "mint": ["parsley", "chamomile"],
    "rosemary": ["basil", "pumpkin"],
    "thyme": ["basil"],
    "oregano": ["mint"],
    "sage": ["basil", "rue", "cucumber"],
    "dill": ["carrot", "fennel", "tomato"],
    "fennel": ["tomato", "bean", "pepper", "caraway", "dill"],
    "cilantro": ["fennel", "dill"],
    "parsley": ["mint", "lettuce"],
    "chives": ["bean", "pea"],
}


def get_good_companions(herb_name):
    """Return a list of good companion plants for the given herb."""
    return list(GOOD_COMPANIONS.get(herb_name.lower().strip(), []))


def get_bad_companions(herb_name):
    """Return a list of plants to avoid near the given herb."""
    return list(BAD_COMPANIONS.get(herb_name.lower().strip(), []))


def are_compatible(herb_a, herb_b):
    """Check if two herbs can be planted together."""
    a_lower = herb_a.lower().strip()
    b_lower = herb_b.lower().strip()

    bad_for_a = BAD_COMPANIONS.get(a_lower, [])
    bad_for_b = BAD_COMPANIONS.get(b_lower, [])

    if b_lower in bad_for_a or a_lower in bad_for_b:
        return False
    return True


def suggest_companions(herb_name, available):
    """From a list of available plants, suggest good companions."""
    herb_lower = herb_name.lower().strip()
    good = set(GOOD_COMPANIONS.get(herb_lower, []))
    bad = set(BAD_COMPANIONS.get(herb_lower, []))
    suggestions = []
    for plant in available:
        plant_lower = plant.lower().strip()
        if plant_lower in good and plant_lower not in bad:
            suggestions.append(plant)
    return sorted(suggestions)


def compatibility_matrix(herb_names):
    """Return a dict of dicts showing compatibility between herbs."""
    matrix = {}
    for a in herb_names:
        matrix[a] = {}
        for b in herb_names:
            if a == b:
                matrix[a][b] = "self"
            elif are_compatible(a, b):
                a_lower = a.lower().strip()
                b_lower = b.lower().strip()
                good_for_a = GOOD_COMPANIONS.get(a_lower, [])
                if b_lower in good_for_a:
                    matrix[a][b] = "good"
                else:
                    matrix[a][b] = "neutral"
            else:
                matrix[a][b] = "bad"
    return matrix
