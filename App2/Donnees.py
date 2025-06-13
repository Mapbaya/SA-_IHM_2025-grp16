import json
import os

class Donnees:

    def __init__(self) -> None:
        # Obtenir le répertoire du script actuel
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        chemin_fichier = os.path.join("..", "App1", "list", "liste_produits_original.json")
        
        # Debug - afficher les chemins pour vérification
        print(f"Répertoire courant : {os.getcwd()}")
        print(f"Chemin relatif : {chemin_fichier}")
        print(f"Chemin absolu : {os.path.abspath(chemin_fichier)}")
        
        with open(chemin_fichier, "r", encoding="utf-8") as f: data = json.load(f)


        # Mettre à jour la clé "Tout" avec tous les éléments des autres listes
        data["Tout"] = []

        for key, items in data.items():
            if key != "Tout":
                data["Tout"].extend(items)

        # Supprimer les doublons tout en gardant l'ordre
        data["Tout"] = list(dict.fromkeys(data["Tout"]))

        # Sauvegarder dans le même fichier (ou un nouveau)
        with open("donnees.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        #Attributs liste données
        self.listCategories : list = list(data.keys())
        self.listProduitsTotal : dict = {}
        self.list_prod_checked : list = []

                
        for category, items in data.items():
            
            self.listProduitsTotal[category] = items 


if __name__ == '__main__':
    data : Donnees = Donnees()
    print(f"Categories : {data.listCategories}\n")
    print(f"Produits : {data.listProduitsTotal}")
    print(data.list_prod_checked)

    