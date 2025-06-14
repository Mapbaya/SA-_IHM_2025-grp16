
import json
from collections import deque
import os

class Graphe:
    def __init__(self):
        self.lettres = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ['AA', 'AB', 'AC', 'AD', 'AE']
        self.lignes = range(1, 24)
        self.sommets = [f"{col}{row}" for col in self.lettres for row in self.lignes]
        self.chemin_dir = "chemins_cache"
        os.makedirs(self.chemin_dir, exist_ok=True)

        # zones_accessibles.json retiré — tout sommet est accessible par défaut sauf s'il est bloqué
        self.interdits_droite = ['A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A2', 'A20', 'A21', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'AC10', 'AC11', 'AC12', 'AC13', 'AC14', 'AC15', 'AC16', 'AC17', 'AC18', 'AC19', 'AC2', 'AC20', 'AC21', 'AC3', 'AC4', 'AC5', 'AC6', 'AC7', 'AC8', 'AC9', 'AE10', 'AE11', 'AE12', 'AE13', 'AE14', 'AE15', 'AE16', 'AE17', 'AE18', 'AE19', 'AE2', 'AE20', 'AE21', 'AE3', 'AE4', 'AE5', 'AE6', 'AE7', 'AE8', 'AE9', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15', 'E16', 'E17', 'E18', 'E19', 'E2', 'E20', 'E21', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'G19', 'G20', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'K10', 'K11', 'K12', 'K13', 'K14', 'K15', 'K16', 'K17', 'K18', 'K19', 'K20', 'K3', 'K4', 'K5', 'K6', 'K7', 'K8', 'K9', 'O10', 'O11', 'O12', 'O13', 'O14', 'O15', 'O16', 'O17', 'O18', 'O19', 'O20', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8', 'O9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'R19', 'R20', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9']
        self.interdits_gauche = ['A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A2', 'A20', 'A21', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'AC10', 'AC11', 'AC12', 'AC13', 'AC14', 'AC15', 'AC16', 'AC17', 'AC18', 'AC19', 'AC2', 'AC20', 'AC21', 'AC3', 'AC4', 'AC5', 'AC6', 'AC7', 'AC8', 'AC9', 'AE10', 'AE11', 'AE12', 'AE13', 'AE14', 'AE15', 'AE16', 'AE17', 'AE18', 'AE19', 'AE2', 'AE20', 'AE21', 'AE3', 'AE4', 'AE5', 'AE6', 'AE7', 'AE8', 'AE9', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15', 'E16', 'E17', 'E18', 'E19', 'E2', 'E20', 'E21', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'H10', 'H11', 'H12', 'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19', 'H20', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'L10', 'L11', 'L12', 'L13', 'L14', 'L15', 'L16', 'L17', 'L18', 'L19', 'L20', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'P10', 'P11', 'P12', 'P13', 'P14', 'P15', 'P16', 'P17', 'P18', 'P19', 'P20', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'S10', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19', 'S20', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9']
        self.interdits_haut = ['AA10', 'AA11', 'AA12', 'AA13', 'AA14', 'AA15', 'AA16', 'AA17', 'AA18', 'AA19', 'AA20', 'AB10', 'AB11', 'AB12', 'AB13', 'AB14', 'AB15', 'AB16', 'AB17', 'AB18', 'AB19', 'AB20', 'G20', 'G21', 'G22', 'K20', 'K21', 'K22', 'O20', 'O21', 'O22', 'R20', 'R21', 'R22', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20', 'W10', 'W11', 'W12', 'W13', 'W14', 'W15', 'W16', 'W17', 'W18', 'W19', 'W20', 'X10', 'X11', 'X12', 'X13', 'X14', 'X15', 'X16', 'X17', 'X18', 'X19', 'X20', 'Y10', 'Y11', 'Y12', 'Y13', 'Y14', 'Y15', 'Y16', 'Y17', 'Y18', 'Y19', 'Y20', 'Z10', 'Z11', 'Z12', 'Z13', 'Z14', 'Z15', 'Z16', 'Z17', 'Z18', 'Z19', 'Z20']
        self.interdits_bas = ['AA10', 'AA11', 'AA12', 'AA13', 'AA14', 'AA15', 'AA16', 'AA17', 'AA18', 'AA19', 'AA20', 'AB10', 'AB11', 'AB12', 'AB13', 'AB14', 'AB15', 'AB16', 'AB17', 'AB18', 'AB19', 'AB20', 'AC21', 'AC22', 'AC23', 'AD21', 'AD22', 'AD23', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20', 'W10', 'W11', 'W12', 'W13', 'W14', 'W15', 'W16', 'W17', 'W18', 'W19', 'W20', 'X10', 'X11', 'X12', 'X13', 'X14', 'X15', 'X16', 'X17', 'X18', 'X19', 'X20', 'Y10', 'Y11', 'Y12', 'Y13', 'Y14', 'Y15', 'Y16', 'Y17', 'Y18', 'Y19', 'Y20', 'Z10', 'Z11', 'Z12', 'Z13', 'Z14', 'Z15', 'Z16', 'Z17', 'Z18', 'Z19', 'Z20']

    def split_coord(self, s):
        for i in range(len(s)):
            if s[i].isdigit():
                return s[:i], int(s[i:])
        return s, -1

    def voisins(self, s):
        col, row = self.split_coord(s)
        voisins_list = []
        if col not in self.lettres:
            return []
        idx = self.lettres.index(col)
        directions = [
            (-1,0, self.interdits_gauche),  # aller à gauche interdit depuis ici
            (1,0, self.interdits_droite),   # aller à droite interdit depuis ici
            (0,-1, self.interdits_haut),    # monter interdit depuis ici
            (0,1, self.interdits_bas),      # descendre interdit depuis ici
        ]
        for dx, dy, blocage in directions:
            ni, nj = idx + dx, row + dy
            if 0 <= ni < len(self.lettres) and 1 <= nj <= 23:
                voisin = f"{self.lettres[ni]}{nj}"
                if voisin in self.sommets and s not in blocage:
                    voisins_list.append(voisin)
        return voisins_list

    def dijkstra(self, depart, arrivee):
        dist = {s: float('inf') for s in self.sommets}
        precedent = {}
        dist[depart] = 0
        file = deque([depart])

        while file:
            courant = file.popleft()
            for voisin in self.voisins(courant):
                if dist[courant] + 1 < dist[voisin]:
                    dist[voisin] = dist[courant] + 1
                    precedent[voisin] = courant
                    file.append(voisin)

        chemin = []
        courant = arrivee
        while courant in precedent:
            chemin.insert(0, courant)
            courant = precedent[courant]
        if chemin:
            chemin.insert(0, depart)
        return chemin

    def obtenir_chemin(self, depart, arrivee):
        if depart not in self.sommets:
            print(f"Le point de départ {depart} est inaccessible.")
            return []
        if arrivee not in self.sommets:
            print(f"Le point d'arrivée {arrivee} est inaccessible.")
            return []

        chemin_fichier = os.path.join(self.chemin_dir, f"{depart}_vers_{arrivee}.json")
        if os.path.exists(chemin_fichier):
            with open(chemin_fichier, "r", encoding="utf-8") as f:
                return json.load(f)

        chemin = self.dijkstra(depart, arrivee)
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            json.dump(chemin, f, indent=2, ensure_ascii=False)
        return chemin

    def obtenir_chemin_intelligent(self, depart, arrivee):
        if depart not in self.sommets:
            print(f"Le point de départ {depart} est inaccessible.")
            return []

        if arrivee in self.sommets:
            return self.obtenir_chemin(depart, arrivee)

        print(f"{arrivee} est inaccessible. Recherche d'une case voisine accessible...")

        col, row = self.split_coord(arrivee)
        if col not in self.lettres:
            return []

        idx = self.lettres.index(col)
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for dx, dy in directions:
            ni, nj = idx + dx, row + dy
            if 0 <= ni < len(self.lettres) and 1 <= nj <= 23:
                voisin = f"{self.lettres[ni]}{nj}"
                if voisin in self.sommets:
                    print(f"Chemin détourné vers voisin accessible : {voisin}")
                    return self.obtenir_chemin(depart, voisin)

        print(f"Aucune case accessible autour de {arrivee}.")
        return []

# Test
if __name__ == "__main__":
    g = Graphe()
    chemin = g.obtenir_chemin_intelligent("W22", "H14")
    print(" → ".join(chemin) if chemin else "Aucun chemin possible.")