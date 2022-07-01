from abc import ABCMeta, abstractmethod


class BaseMapper(metaclass=ABCMeta):

    def __init__(self, connection) -> None:
        self.connection = connection
        self.cursor = connection.cursor()

    @property
    @abstractmethod
    def tablename(self):
        pass

    @property
    @abstractmethod
    def model(self):
        pass

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        column_names = [description_info[0] for description_info in self.cursor.description]
        result = []

        for values in self.cursor.fetchall():
            object = self.model(**{column_names[i]: values[i] for i, _ in enumerate(values)})

            result.append(object)
        return result

    def find_by_id(self, id):
        statement = f'SELECT id, name from {self.tablename} WHERE id =?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()

        try:
            id, name = result
            return self.model(id=id, name=name)
        except Exception as e:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, **schema):
        statement = f'INSERT INTO {self.tablename} ({",".join(schema.keys())}) VALUES (?)'
        self.cursor.execute(statement, (",".join(schema.values()),))
        try:
            self.connection.commit()
        except Exception as e:
            raise DBCommitException(e.args)

    def update(self, object, **schema):
        schema = {str(key) + '=?': value for key, value in schema.items()}
        statement = f'UPDATE {self.tablename} SET {",".join(schema.keys())} WHERE id=?'
        self.cursor.execute(statement, (",".join(schema.values()), object.id))
        try:
            self.connection.commit
        except Exception as e:
            raise DBUpdateException(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit
        except Exception as e:
            raise DBDeleteException(e.args)


class DBCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'DB commit error: {message}')


class DBUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'DB update error: {message}')


class DBDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'DB delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found : {message}')
