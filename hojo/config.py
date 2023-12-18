class Config:
    _instance = None
    _configurations = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def set(cls, key, value):
        cls.instance()._configurations[key] = value

    @classmethod
    def get(cls, key):
        return cls.instance()._configurations.get(key)

    @classmethod
    def reset(cls):
        cls._instance = None
        cls._configurations = {}
