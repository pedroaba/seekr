import datetime


def get_default_config():
    return {
        "version": "v1",
        "created_at": datetime.datetime.now().isoformat(sep=" "),
        "updated_at": datetime.datetime.now().isoformat(sep=" "),
        "ignores_paths": [
        ]
    }