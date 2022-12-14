class Model:
    def __init__(self, data=None):
        self.set_attributes(data)

    def set_attributes(self, data):
        if not data:
            return

        for attribute, value in data.items():
            setattr(self, attribute, value)

    @staticmethod
    def collection():
        pass

    @staticmethod
    def primary_key():
        return '_id'