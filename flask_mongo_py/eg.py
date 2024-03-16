from pymongo import MongoClient

class Collection:
    def __init__(self, client, name):
        self.client = client
        self.name = name
        if name in client["motor"].list_collection_names():
            self.collection = client["motor"][name]
            self.initialize_attributes()
        else:
            raise ValueError(f"Collection '{name}' does not exist in the database.")

    def display(self):
        documents = self.get_documents()
        print(f"{self.name.capitalize()} Documents:")
        for document in documents:
            print(document)

    def initialize_attributes(self):
        pass

    def get_documents(self):
        documents = self.collection.find()
        return documents

class SteelCollection(Collection):
    def __init__(self, client):
        super().__init__(client, "steel")

class MagnetCollection(Collection):
    def __init__(self, client):
        super().__init__(client, "magnet")


class WireCollection(Collection):
    def __init__(self, client):
        super().__init__(client, "wire")

    def get_documents(self):
        wire_documents = super().get_documents()
        return list(wire_documents)
    
    def get_swg_documents(self):
        swg_documents = self.client["motor"]["swg1"].find()
        return list(swg_documents)

    def display(self):
        documents = self.get_documents()
        swg_documents = self.get_swg_documents()
        print(f"{self.name.capitalize()} Documents:")
        for document in documents:
            print(document)

        while True:
            value = input("Enter the SWG value (-1 to exit): ")
            if value == "-1":
                break
            else:
                found = False#exact swg value found is set to false
                nearest_swg = None #nearest swg value is stored based on input value
                nearest_swg_doc = None#nearest swg doc is stored
                min_difference = float('inf') #set to infinity and store the diff b/w the i/p value and swg values during search
                for doc in swg_documents:#outer loop - for each doc
                    for swg_value_str in doc:# inner loop - for each key
                        if swg_value_str != "_id" and swg_value_str.replace('.', '').isdigit():#removing periods becoz not specifically related to data representations such as JSON or MongoDB documents
                            swg_value = float(swg_value_str)
                            difference = abs(float(value) - swg_value)#finds abs diff b/w i/p value and swg
                            if difference < min_difference:#checks which val is min (after sub the i/p from the swg value)
                                min_difference = difference
                                nearest_swg = swg_value
                                nearest_swg_doc = doc
                            if difference == 0:
                                found = True
                                print(f"Value for SWG {swg_value}: {doc[swg_value_str]}")
                                break
                if not found and nearest_swg is not None:
                    print(f"Nearest SWG value: {nearest_swg}")
                    print(f"Value for SWG {nearest_swg}: {nearest_swg_doc[str(nearest_swg)]}")
                elif not found:
                    print("Value not found for the entered SWG.")



class CopperIronCollection(Collection):
    def __init__(self, client):
        super().__init__(client, "copper_iron")

if __name__ == '__main__':
    MONGO_URI = "mongodb+srv://guselvaraanni:selvaraanni24@cluster0.03ahigd.mongodb.net/"
    client = MongoClient(MONGO_URI)

    while True:
        key = input("Enter the key (-1 to exit): ")
        
        if key == "-1":
            break
        
        if key in ["N42", "M250-35A", "wire", "copper_iron"]:
            if key == "N42":
                magnet = MagnetCollection(client)
                magnet.display()
            elif key == "M250-35A":
                steel = SteelCollection(client)
                steel.display()
            elif key == "wire":
                wire = WireCollection(client)
                wire.display()
            elif key == "copper_iron":
                copper_iron = CopperIronCollection(client)
                copper_iron.display()
        else:
            found = False
            for collection_name in client["motor"].list_collection_names():
                collection = client["motor"][collection_name]
                document = collection.find_one({"key": key})
                if document:
                    print(f"Value for {key}: {document['value']}")
                    found = True
                    break
            if not found:
                print("Key not found in any collection.")
