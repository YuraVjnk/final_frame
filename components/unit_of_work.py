import threading


# Архитектурный системный паттерн - UnitOfWork

class UnitOfWork:
    '''
    Паттерн Юнит оф Ворк
    '''
    # Работает с конкретным потоком
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, MapperRegistry):
        self.MapperRegistry = MapperRegistry

    def register_new(self, obj, schema):
        self.new_objects.append({'object': obj, 'schema': schema})

    def register_dirty(self, obj, schema):
        self.dirty_objects.append({'object': obj, 'schema': schema})

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

        self.new_objects.clear()
        self.dirty_objects.clear()
        self.removed_objects.clear()

    def insert_new(self):
        print(self.new_objects)
        for obj in self.new_objects:
            print(obj)
            print(f'Вывожу {self.MapperRegistry}')
            self.MapperRegistry.get_mapper(obj['object']).insert(**obj['schema'])

    def update_dirty(self):
        for obj in self.dirty_objects:
            self.MapperRegistry.get_mapper(obj['object']).update(**obj['schema'])

    def delete_removed(self):
        for obj in self.removed_objects:
            self.MapperRegistry.get_mapper(obj).delete(obj)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:

    def mark_new(self, schema):
        UnitOfWork.get_current().register_new(self, schema)

    def mark_dirty(self, schema):
        UnitOfWork.get_current().register_dirty(self, schema)

    def mark_removed(self, schema):
        UnitOfWork.get_current().register_removed(self, schema)
