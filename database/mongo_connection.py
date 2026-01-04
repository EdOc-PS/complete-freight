from pymongo import MongoClient

class MongoConnection:
    _client = None

    @classmethod
    def get_database(cls):
        if cls._client is None:
            cls._client = MongoClient(
                "mongodb+srv://tomador:KVEoqBpAwH6YpRiv@edoc-cluster.pv0lxby.mongodb.net/?appName=edoc-cluster"
            )
        return cls._client["complete_freight"]

# 🔥 ISSO RESOLVE SEU ERRO
db = MongoConnection.get_database()
