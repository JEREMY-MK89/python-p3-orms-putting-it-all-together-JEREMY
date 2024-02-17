# lib/dog.py

import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        if self.id is None:
            self._insert()
        else:
            self._update()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        id, name, breed = row
        return cls(name, breed, id)

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs WHERE name = ?
        """
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM dogs WHERE id = ?
        """
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            return cls.create(name, breed)

    def _insert(self):
        sql = """
            INSERT INTO dogs (name, breed) VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        self.id = CURSOR.lastrowid
        CONN.commit()

    def _update(self):
        sql = """
            UPDATE dogs SET name = ?, breed = ? WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()

    def update(self):
        self._update()
