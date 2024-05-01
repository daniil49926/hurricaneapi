

class DependenceProtocol:
    _inst = None
    def __init__(self):
        env_file_path: str = '.env.hurricaneapi'  # noqa

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._inst, cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
        return cls._inst
