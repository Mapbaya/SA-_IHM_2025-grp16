"""
Modèle de données pour le plan de magasin.

Ce module gère les données du plan, notamment :
- Le chargement et la sauvegarde du plan
- Les informations sur les zones
- Les produits associés aux zones
"""

import os
import json
from PyQt6.QtGui import QImage
from config import DOSSIER_PROJETS


class ModelePlan:
    """
    Modèle de données pour le plan de magasin.
    
    Gère l'état et les données du plan, y compris :
    - L'image du plan
    - Les zones définies
    - Les produits par zone
    """
    
    
    def __init__(self):
        """Initialise un nouveau modèle de plan."""
        self.image_plan = None
        self.zones = {}  # Dictionnaire des zones avec leurs produits
        self.nom_projet = None
        self.chemin_plan = None
        self.plan_cases_magasin()
        
    def charger_plan(self, chemin):
        """
        Charge une nouvelle image de plan.
        
        Args:
            chemin: Chemin vers le fichier image du plan
            
        Raises:
            ValueError: Si le fichier est invalide ou illisible
        """
        # Vérification du fichier
        if not os.path.isfile(chemin):
            raise ValueError(f"Le fichier n'existe pas : {chemin}")
            
        # Chargement de l'image
        image = QImage(chemin)
        if image.isNull():
            raise ValueError(f"Format d'image non supporté : {chemin}")
            
        # Mise à jour du modèle
        self.image_plan = image
        self.chemin_plan = chemin
        self.zones.clear()
        
    def charger_projet(self, chemin):
        """
        Charge un projet existant.
        
        Args:
            chemin: Chemin vers le fichier de configuration du projet
            
        Raises:
            ValueError: Si le projet est invalide ou corrompu
        """
        try:
            # Lecture du fichier de configuration
            with open(chemin, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # Validation de la structure
            if not all(k in config for k in ['nom', 'chemin_plan', 'zones']):
                raise ValueError("Format de projet invalide")
                
            # Chargement du plan
            self.charger_plan(config['chemin_plan'])
            
            # Mise à jour du modèle
            self.nom_projet = config['nom']
            self.zones = config['zones']
            
        except json.JSONDecodeError:
            raise ValueError("Fichier de projet corrompu")
        except Exception as e:
            raise ValueError(f"Erreur lors du chargement : {str(e)}")
            
    def sauvegarder(self, chemin):
        """
        Sauvegarde l'état actuel du projet.
        
        Args:
            chemin: Chemin où sauvegarder le projet
            
        Raises:
            ValueError: Si la sauvegarde échoue
        """
        if not self.image_plan:
            raise ValueError("Aucun plan à sauvegarder")
            
        try:
            # Préparation des données
            config = {
                'nom': self.nom_projet or os.path.splitext(os.path.basename(chemin))[0],
                'chemin_plan': self.chemin_plan,
                'zones': self.zones
            }
            
            # Sauvegarde du fichier
            with open(chemin, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            raise ValueError(f"Erreur lors de la sauvegarde : {str(e)}")
            
    def definir_produits_zone(self, zone, produits):
        """
        Définit les produits pour une zone donnée.
        
        Args:
            zone: Identifiant de la zone (ex: "A1")
            produits: Liste des produits à placer dans la zone
        """
        if produits:
            self.zones[zone] = produits
        elif zone in self.zones:
            del self.zones[zone]
            
    def obtenir_produits_zone(self, zone):
        """
        Récupère les produits d'une zone donnée.
        
        Args:
            zone: Identifiant de la zone (ex: "A1")
            
        Returns:
            Liste des produits dans la zone
        """
        return self.zones.get(zone, [])

    
    def plan_cases_magasin(self):
        # Construction du dictionnaire correspondant au plan par defaut"
        self.dict_cases : dict = { 
                             "Légumes": ["H3", "I3", "J3", "K3", "H4", "I4", "J4", "K4", "H5", "I5", "J5", "K5", "H6", "I6", "J6", "K6", "H7", "I7", "J7", "K7", "H8", "I8", "J8", "K8", "H9", "I9", "J9", "K9", "H10", "I10", "J10", "K10", "H11", "I11", "J11", "K11"],
         
                            "Fruits": ["H3", "I3", "J3", "K3", "H4", "I4", "J4", "K4", "H5", "I5", "J5", "K5", "H6", "I6", "J6", "K6", "H7", "I7", "J7", "K7", "H8", "I8", "J8", "K8", "H9", "I9", "J9", "K9", "H10", "I10", "J10", "K10", "H11", "I11", "J11", "K11"],
         
                            "Poissons": ['B1', 'C1', 'B2', 'C2', 'A3', 'B3'],
                            
                            "Fromages": ['E1', 'F1', 'G1', 'H1', 'E2', 'F2', 'G2', 'H2'],
                            
                            "Viandes": ['H1', 'I1', 'J1', 'K1', 'L1', 'M1', 'N1', 'O1', 'P1', 'Q1', 'R1', 'R2', 'S2', 'T2', 'U2', 'V2', 'W2', 'X2', 'Y2', 'Z2', 'AA2', 'AB2', 'AC2', 'AD2', "F3", "G3", "F4", "G4", "F5", "G5", "F6", "G6", "F7", "G7", "F8", "G8", "F9", "G9", "F10", "G10", "F11", "G11", 'E3', 'E4', 'E5'],
                            
                            "Épicerie": ["G13", "H13", "I13", "J13", "K13", "L13", "G14", "H14", "I14", "J14", "K14", "L14", "G15", "H15", "I15", "J15", "K15", "L15", "G16", "H16", "I16", "J16", "K16", "L16", "G17", "H17", "I17", "J17", "K17", "L17", "G18", "H18", "I18", "J18", "K18", "L18", "G19", "H19", "I19", "J19", "K19", "L19", "E16", "F16", "E17", "F17", "E18", "F18", "E19", "F19"],
                            
                            "Épicerie sucrée": ["G13", "H13", "I13", "J13", "K13", "L13", "G14", "H14", "I14", "J14", "K14", "L14", "G15", "H15", "I15", "J15", "K15", "L15", "G16", "H16", "I16", "J16", "K16", "L16", "G17", "H17", "I17", "J17", "K17", "L17", "G18", "H18", "I18", "J18", "K18", "L18", "G19", "H19", "I19", "J19", "K19", "L19", "E16", "F16", "E17", "F17", "E18", "F18", "E19", "F19"],
                            
                            "Petit déjeuner": ["O3", "O4", "O5", "O6", "O7", "O8", "O9", "O10", "O11", "Y3", "Z3", "AA3", "AB3", "AC3"],

                            "Rayon frais": ["A4", "B4", "C4", "D4", "A5", "B5", "C5", "D5", "A6", "B6", "C6", "D6", "A7", "B7", "C7", "D7", "A8", "B8", "C8", "D8", "A9", "B9", "C9", "D9", "A10", "B10", "C10", "D10", "A11", "B11", "C11", "D11"],

                            "Crèmerie": ['E6', 'E7', 'E8', 'E9', 'E10', 'E11'],
                            
                            "Conserves": ["G13", "H13", "I13", "J13", "K13", "L13", "G14", "H14", "I14", "J14", "K14", "L14", "G15", "H15", "I15", "J15", "K15", "L15", "G16", "H16", "I16", "J16", "K16", "L16", "G17", "H17", "I17", "J17", "K17", "L17", "G18", "H18", "I18", "J18", "K18", "L18", "G19", "H19", "I19", "J19", "K19", "L19", "E16", "F16", "E17", "F17", "E18", "F18", "E19", "F19"],
                            
                            "Apéritifs": ["D13", "E13", "D14", "E14", "D15", "E15", "D16", "E16", "D17", "E17", "D18", "E18", "D19", "E19", 'F13', 'F14', 'F15',"A13", "B13", "A14", "B14", "A15", "B15", "A16", "B16", "A17", "B17", "A18", "B18", "A19", "B19", "A20", "B20", "A21", "B21", "A22", "B22"],
                            
                            "Boissons": ["C13", "C14", "C15", "C16", "C17", "C18", "C19", "B22", "C22", "D22", "E22", "F22", "G22", 'G21'],
                            
                            "Articles Maison": ["Y4", "Z4", "AA4", "AB4", "AC4", "Y5", "Z5", "AA5", "AB5", "AC5", "Y6", "Z6", "AA6", "AB6", "AC6", "Y7", "Z7", "AA7", "AB7", "AC7", "Y8", "Z8", "AA8", "AB8", "AC8", "Y9", "Z9", "AA9", "AB9", "AC9", "Y10", "Z10", "AA10", "AB10", "AC10", "Y11", "Z11", "AA11", "AB11", "AC11", "Y14", "Z14", "AA14", "AB14", "AC14", "Y15", "Z15", "AA15", "AB15", "AC15", "Y16", "Z16", "AA16", "AB16", "AC16", "Y17", "Z17", "AA17", "AB17", "AC17", "Y18", "Z18", "AA18", "AB18", "AC18", "Y19", "Z19", "AA19", "AB19", "AC19", "Y20", "Z20", "AA20", "AB20", "AC20","X21", "Y21", "Z21", "AA21", "AB21", "AC21", "AD21", "AE21", "AE9", "AE10", "AE11", "AE12", "AE13", "AE14", "AE15", "AE16", "AE17", "AE18", "AE19", "AE20"],
                            
                            "Hygiène": ["R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "S3", "T3", "U3", "S4", "T4", "U4", "S5", "T5", "U5", "S6", "T6", "U6", "S7", "T7", "U7", "S8", "T8", "U8", "S9", "T9", "U9", "S10", "T10", "U10", "S11", "T11", "U11","AE3", "AE4", "AE5", "AE6", "AE7", "AE8"],
                            
                            "Bureau": ["Y4", "Z4", "AA4", "AB4", "AC4", "Y5", "Z5", "AA5", "AB5", "AC5", "Y6", "Z6", "AA6", "AB6", "AC6", "Y7", "Z7", "AA7", "AB7", "AC7", "Y8", "Z8", "AA8", "AB8", "AC8", "Y9", "Z9", "AA9", "AB9", "AC9", "Y10", "Z10", "AA10", "AB10", "AC10", "Y11", "Z11", "AA11", "AB11", "AC11", "Y14", "Z14", "AA14", "AB14", "AC14", "Y15", "Z15", "AA15", "AB15", "AC15", "Y16", "Z16", "AA16", "AB16", "AC16", "Y17", "Z17", "AA17", "AB17", "AC17", "Y18", "Z18", "AA18", "AB18", "AC18", "Y19", "Z19", "AA19", "AB19", "AC19", "Y20", "Z20", "AA20", "AB20", "AC20","X21", "Y21", "Z21", "AA21", "AB21", "AC21", "AD21", "AE21", "AE9", "AE10", "AE11", "AE12", "AE13", "AE14", "AE15", "AE16", "AE17", "AE18", "AE19", "AE20"],
                            
                            "Animaux": ["P3", "Q3", "P4", "Q4", "P5", "Q5", "P6", "Q6", "P7", "Q7", "P8", "Q8", "P9", "Q9", "P10", "Q10", "P11", "Q11"],
                            
                            "Surgelés" : ["L3", "M3", "N3", "L4", "M4", "N4", "L5", "M5", "N5", "L6", "M6", "N6", "L7", "M7", "N7", "L8", "M8", "N8", "L9", "M9", "N9", "L10", "M10", "N10", "L11", "M11", "N11"],
                            
                            "Saisonnier" : ["V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11", "Y11", "Z11", "AA11", "AB11", "AC11", "Y12", "Z12", "AA12", "AB12", "AC12", "Y13", "Z13", "AA13", "AB13", "AC13", "Y14", "Z14", "AA14", "AB14", "AC14", "V13", "V14", "V15", "V16", "V17", "V18", "V19"],
                            
                            "Textile" : ["M13", "N13", "O13", "P13", "R13", "T13", "U13", "M14", "N14", "O14", "P14", "R14", "T14", "U14", "M15", "N15", "O15", "P15", "R15", "T15", "U15", "M16", "N16", "O16", "P16", "R16", "T16", "U16", "M17", "N17", "O17", "P17", "R17", "T17", "U17", "M18", "N18", "O18", "P18", "T18", "U18", "M19", "N19", "O19", "P19", "T19", "U19", 'Q16', 'Q17', 'S16', 'S17'],
                            
                            "Caisses" : ["H20", "I20", "J20", "K20", "L20", "M20", "N20", "O20", "P20", "Q20", "R20", "S20", "T20", "U20", "H21", "I21", "J21", "K21", "L21", "M21", "N21", "O21", "P21", "Q21", "R21", "S21", "T21", "U21", "H22", "I22", "J22", "K22", "L22", "M22", "N22", "O22", "P22", "Q22", "R22", "S22", "T22", "U22"]
                            
                            
                            }
        
        
        
        
    def liste_cases_occupees(self):
        cases_occupees : list = []
                
        for item, list_cases in self.dict_cases.items():
            for case in list_cases:
                if len(cases_occupees) == 0:
                    cases_occupees.append(case)
                else:
                    if case not in cases_occupees:
                        cases_occupees.append(case)
        return cases_occupees
    
    
    def liste_cases_par_rayon(self, nom_rayon : str, dict_cases : dict):
        cases_rayon : list = []
        if nom_rayon in dict_cases:
            cases_rayon = dict_cases[nom_rayon]
        else:
            print("Le rayon n'est pas dans le magasin")
        return cases_rayon
        
    
    def generation_cases_tableau_complet(self, nb_col, nb_lignes):
        liste_cases = []
        
        for i in range(nb_col):
            for j in range(nb_lignes):
                if (i < 26) :
                    coord : str = chr(ord('A') + i) + str(j + 1)
                    liste_cases.append(coord)
                else:
                    coord : str = 'A' + chr(ord('A') + i % 26) + str(j + 1)
                    liste_cases.append(coord)
        
        return liste_cases
    
    
    def cases_vides(self, tableau_complet, tableau_cases_occupees):
        liste_complete = tableau_complet
        liste_a_soustraire = tableau_cases_occupees
        
        # conversion en set des elements a suppriemr
        set_elements_a_suppr = set(liste_a_soustraire)
        
        # liste des cases vides
        liste_cases_vides = [li for li in liste_complete if li not in set_elements_a_suppr]
        
        return liste_cases_vides    
    

# if __name__ == '__main__':
    
#     def generation_cases_tableau_complet(nb_col, nb_lignes):
#         liste_cases = []
        
#         for i in range(nb_col):
#             for j in range(nb_lignes):
#                 if (i < 26) :
#                     coord : str = chr(ord('A') + i) + str(j + 1)

#                     liste_cases.append(coord)
#                 else:
#                     coord : str = 'A' + chr(ord('A') + i % 26) + str(j + 1)

#                     liste_cases.append(coord)
        
#         return liste_cases
    
    
#     def cases_vides(tableau_complet, tableau_cases_occupees):
#         liste_complete = tableau_complet
#         liste_a_soustraire = tableau_cases_occupees
        
#         # conversion en set des elements a suppriemr
#         set_elements_a_suppr = set(liste_a_soustraire)
        
#         # liste des cases vides
#         liste_cases_vides = [li for li in liste_complete if li not in set_elements_a_suppr]
        
#         return liste_cases_vides    
    
    
    
#     listessai = generation_cases_tableau_complet(31, 23)

    
#     liste_a_supprimer = ['U19', 'U20', 'U21', 'U22', 'U23', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20', 'V21', 'V22', 'V23', 'W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10', 'W11', 'W12', 'W13', 'W14', 'W15', 'W16', 'W17', 'W18', 'W19', 'W20', 'W21', 'W22', 'W23', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10', 'X11', 'X12', 'X13', 'X14', 'X15', 'X16', 'X17', 'X18', 'X19', 'X20', 'X21', 'X22', 'X23', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8', 'Y9', 'Y10', 'Y11', 'Y12', 'Y13', 'Y14', 'Y15', 'Y16', 'Y17', 'Y18', 'Y19', 'Y20', 'Y21', 'Y22', 'Y23', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8', 'Z9', 'Z10', 'Z11', 'Z12', 'Z13', 'Z14', 'Z15', 'Z16', 'Z17', 'Z18', 'Z19', 'Z20', 'Z21', 'Z22', 'Z23', 'AA1', 'AA2', 'AA3', 'AA4', 'AA5', 'AA6', 'AA7', 'AA8', 'AA9', 'AA10', 'AA11', 'AA12', 'AA13', 'AA14', 'AA15', 'AA16', 'AA17', 'AA18', 'AA19', 'AA20', 'AA21', 'AA22', 'AA23', 'AB1', 'AB2', 'AB3', 'AB4', 'AB5', 'AB6', 'AB7', 'AB8', 'AB9', 'AB10', 'AB11', 'AB12', 'AB13', 'AB14', 'AB15', 'AB16', 'AB17', 'AB18', 'AB19', 'AB20', 'AB21', 'AB22', 'AB23', 'AC1', 'AC2']
    
#     liste_resultat = cases_vides(listessai, liste_a_supprimer)
#     print(liste_resultat)
    

        

