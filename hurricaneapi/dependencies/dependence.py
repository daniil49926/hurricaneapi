

class DependenceProtocol:
    _inst = None
    def __init__(self):
        self.env_file_path: str = '.env.hurricaneapi'
        self.env_var: dict[str, str] = {}
        with open(self.env_file_path, 'r') as file:
            while line := file.readline().replace(' ', '').replace('\n', '').split('='):
                if len(line) != 2:
                    break
                self.env_var[line[0]] = line[1]

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._inst, cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
        return cls._inst
