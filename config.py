import os

VERSION = "0.4.2"

MAX_COLLECTION_SIZE = 10000
DEFAULT_HERB_NAME = "Unnamed"
SUPPORTED_EXPORT_FORMATS = ["text", "csv", "json"]

DATA_DIR = os.environ.get("HERB_GARDEN_DATA", os.path.join(os.path.expanduser("~"), ".herb-garden"))
LOG_LEVEL = os.environ.get("HERB_GARDEN_LOG_LEVEL", "INFO")


class Settings:
    show_ids = True
    show_tree_lines = True
    page_size = 50
    sort_ascending = True
    auto_save = False
    data_format = "json"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"unknown setting: {key}")

    def as_dict(self):
        return {
            "show_ids": self.show_ids,
            "show_tree_lines": self.show_tree_lines,
            "page_size": self.page_size,
            "sort_ascending": self.sort_ascending,
            "auto_save": self.auto_save,
            "data_format": self.data_format,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})
