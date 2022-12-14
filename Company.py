from Model import Model


class Company(Model):
    _id = None
    remote_id = None
    name = None
    country = None
    city = None
    address = None
    profile = None
    inn = None
    ogrn = None
    paid_only = None

    @staticmethod
    def collection():
        return 'company'