from modules.database import session


class BaseDBOperationsMixin:

    @classmethod
    def get(cls, **kwargs):
        instance = session.query(cls).filter_by(id=kwargs.get('id')).first()
        if instance:
            return instance
        raise Exception(f'{cls} not found')

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        session.add(instance)
        session.commit()

    @classmethod
    def get_or_create(cls, **kwargs):
        if 'id' not in kwargs:
            raise Exception(f'Cannot search for a {cls} instance without an `id` field')
        instance = session.query(cls).filter_by(id=kwargs.get('id')).first()
        if instance:
            return instance
        instance = cls(**kwargs)
        session.add(instance)
        session.commit()
        return instance

    def update(self, **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs.get(key))
            print(f'[{self}] New `{key}` value is: {getattr(self, key)}')
        session.add(self)
        session.commit()

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.__class__.__name__} object ({self.id})>'
