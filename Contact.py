from Model import Model


class Contact(Model):
    id = None
    name = None
    phone = None
    mobile = None
    fax = None
    icq = None
    skype = None
    remote_id = None

    @staticmethod
    def collection():
        return 'contact'