from herb import Herb
from garden import Garden


def herb_to_dict(herb):
    parent_id = herb.parent.id if herb.parent is not None else None
    return {
        "id": herb.id,
        "name": herb.name,
        "parent_id": parent_id,
    }


def garden_to_dict(garden):
    herbs = []
    for herb in garden.herbs():
        herbs.append(herb_to_dict(herb))
    return {"herbs": herbs}


def herb_from_dict(data):
    herb = Herb(name=data.get("name", ""))
    herb.id = data.get("id", 0)
    return herb


def garden_from_dict(data):
    garden = Garden()
    herb_data = data.get("herbs", [])
    id_map = {}
    for entry in herb_data:
        herb = Herb(name=entry.get("name", ""))
        herb.id = entry.get("id", 0)
        id_map[herb.id] = (herb, entry.get("parent_id"))
        garden._herbs[herb.id] = herb
        if herb.id > garden._counter:
            garden._counter = herb.id
    for herb_id, (herb, parent_id) in id_map.items():
        if parent_id is not None and parent_id in id_map:
            parent_herb = id_map[parent_id][0]
            herb.parent = parent_herb
            parent_herb._children.append(herb)
    return garden
