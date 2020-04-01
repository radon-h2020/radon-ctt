class AbstractModel:

    @classmethod
    def get_parent_type(cls):
        raise NotImplementedError('Not implemented')

    @classmethod
    def get_all(cls):
        raise NotImplementedError('Not implemented')

    @classmethod
    def get_by_uuid(cls, get_uuid):
        raise NotImplementedError('Not implemented')

    @classmethod
    def delete_by_uuid(cls, del_uuid):
        raise NotImplementedError('Not implemented')
