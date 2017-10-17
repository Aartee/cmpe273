import rocksdb

class DBManager():
    """
    Database manager class
    """
    def __init__(self):
        print("INIT FROM DB")
        self.db = rocksdb.DB("db/script.db", rocksdb.Options(create_if_missing=True))

    def get_file(self, key):
        return self.db.get(key)

    def add_file(self, key, value):
        self.db.put(key, value)

    def update_file(self, key, value):
        self.db.put(key, value)

    def delete_file(self, key):
        self.db.delete(key)