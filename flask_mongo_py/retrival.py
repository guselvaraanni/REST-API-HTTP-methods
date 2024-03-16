from pymongo import MongoClient
from bson import ObjectId

class Collection:
    def __init__(self, client, name):
        self.client = client
        self.name = name
        if name in client["motor"].list_collection_names():
            self.collection = client["motor"][name]
            self.initialize_attributes()
        else:
            raise ValueError(f"Collection '{name}' does not exist in the database.")

    def display(self, document_id):
        document = self.get_document(document_id)
        print(f"{self.name.capitalize()} Document:", document)

    def initialize_attributes(self):
        pass

    def get_document(self, document_id):
        try:
            obj_id = ObjectId(document_id)
            document = self.collection.find_one({'_id': obj_id})
            if document:
                return document
            else:
                return {'error': 'Document not found'}
        except Exception as e:
            return {'error': 'Invalid document ID'}

class SteelCollection(Collection):
    def __init__(self, client):
        super().__init__(client, "steel")

class MagnetCollection(Collection):
    def __init__(self, client):
        super().__init__(client, "magnet")

class CopperCollection(Collection):
    def __init__(self, client):
        super().__init__(client, "copper")

class CopperIronCollection(Collection):
    def __init__(self, client):
        super().__init__(client, "copper_iron")

if __name__ == '__main__':
    MONGO_URI = "mongodb+srv://guselvaraanni:selvaraanni24@cluster0.03ahigd.mongodb.net/"
    client = MongoClient(MONGO_URI)

    steel = SteelCollection(client)
    steel.display("65af9ac77392d1d059eda7ff")

    magnet = MagnetCollection(client)
    magnet.display("65af8520199ac033db4712b7")

    copper = CopperCollection(client)
    copper.display("65af9dae85c79cd2480a2499")

    copper_iron = CopperIronCollection(client)
    copper_iron.display("65af9a59b507d7938b71552e")
