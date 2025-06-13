import json

class Donnees:

    def __init__(self) -> None:

        with open("./liste_produits.json", "r", encoding="utf-8") as f: data = json.load(f)
        
        self.listCategories : list = list(data.keys())
        self.listProduitsTotal : dict = {}

                
        for category, items in data.items():
            
            self.listProduitsTotal[category] = items 

# if __name__ == '__main__':
#     data : Donnees = Donnees()
#     print(f"Categories : {data.listCategories}\n")
#     print(f"Produits : {data.listProduitsTotal}\n{data.listProduitsTotal['Légumes']}")

    