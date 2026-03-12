from herb import Herb


class Garden:
    def __init__(self):
        self._herbs = {}
        self._counter = 0

    def create(self, name, parent_id=None):
        herb = Herb(name)
        self._counter += 1
        herb.id = self._counter
        if parent_id is not None:
            parent = self._herbs[parent_id]
            herb.parent = parent
            parent._children.append(herb)
        self._herbs[herb.id] = herb
        return herb

    def get(self, herb_id):
        return self._herbs[herb_id]

    def roots(self):
        return [h for h in self._herbs.values() if h.parent is None]

    def herbs(self):
        return list(self._herbs.values())
