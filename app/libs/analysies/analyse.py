from utils import utils as utl
from pprint import pprint


class AnalyseData(object):
    def __init__(self, data):
        self.data = data
        self.analyse = {}
        # pprint(self.data)

        self.bvps_analyse()
        self.per_analyse()
        self.dette_analyse()
        self.chiffre_affaire_analyse()
        self.b_graham_function()

    def bvps_analyse(self):
        bvps, index = utl.get_last_value(self.data["BVPS"])
        intraseq_value = self.b_graham_function()
        analyse = ""
        if intraseq_value < float(self.data["PRICE"][index]):
            analyse = "Prix SUR-COTE à sa valeur intrasèque : {} €.".format(
                intraseq_value
            )
        elif intraseq_value > float(self.data["PRICE"][index]):
            analyse = "Prix SOUS-COTE à sa valeur intrasèque : {}€".format(
                intraseq_value
            )
        self.analyse["BVPS"] = analyse

    def per_analyse(self):
        per, index = utl.get_last_value(self.data["PER"])
        analyse = ""
        if per <= 0:
            analyse = "PER %s NégatifG" % per
        elif per >= 17:
            analyse = "PER %s Eleve , Entreprise SUR-COTE." % per
        elif 10 <= per < 17:
            analyse = "PER %s Normal , Entreprise OK." % per
        elif per < 10:
            analyse = "PER %s < 10, Entreprise SOUS-COTE." % per
        self.analyse["PER"] = analyse

    def dette_analyse(self):
        dette, index = utl.get_last_value(self.data["Dette"])
        analyse = ""
        try:
            if 0 < dette <= 2:
                analyse = "Dette Controle"
            elif dette <= 0:
                analyse = "Dette Aucune"
            elif dette > 2:
                analyse = "Dette Eleve"
        except:
            analyse = "Pas de Dette"
        self.analyse["Dette"] = analyse

    def chiffre_affaire_analyse(self):
        chiffre = self.data["Chiffre d'affaires"]
        if chiffre[0] > chiffre[1]:
            analyse = "Chiffre d'affaire en croissance."
        else:
            analyse = "Chiffre d'affaire en décroissance."
        self.analyse["Chiffre d'affaires"] = analyse

    def b_graham_function(self):
        """
        formula : V=(EPS*(7+1g)*4.4)/Y
           EPS: BPA
           7 : Ration cours/bénéfice pour une entreprise sans croissance
           g : taux de croissance raisonnablement attendu pour 7 à 10 prochaines années
           4,4 : le rendement moyen des obligations de sociétés AAA en 1962
           Y : le rendement actuel des obligations de sociétés AAA
        """
        growth = int(float(self.data['Growth']))
        bna, index = utl.get_last_value(self.data["BNA"])
        formula = (bna * (7 + 1 * growth) * 4.4) / utl.get_compagny_yield()
        return round(formula, 2)