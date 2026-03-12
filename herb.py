class Herb:
    _fields = ("name",)
    _registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Herb._registry[cls.__name__] = cls

    def __init__(self, name=""):
        self._id = 0
        self._name = name
        self._parent = None
        self._children = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def children(self):
        return list(self._children)

    def __repr__(self):
        return f"Herb(id={self._id}, name={self._name!r})"
