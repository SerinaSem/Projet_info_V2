from models.employe import Employe
from services.employe_service import *

# Ajouter un employé
e1 = Employe(None, "Dupont", "Emma", "emma.dupont@mail.com", 25, 1)
e2 = Employe(None, "Lemoine", "Sarah", "sarah.lemoine@mail.com", 35, 1)
e3 = Employe(None, "Semmani", "Serina", "serina.semmani@mail.com", 16, 1)
ajouter_employe(e1)
ajouter_employe(e2)
ajouter_employe(e3)

# Voir tous les employés
#employes = recuperer_tous_employes()
#for e in employes:
#    print(e)

# Modifier un employé
#employe_a_modifier = recuperer_employe_par_id(1)
#if employe_a_modifier:
#    employe_a_modifier.email = "emma.nouveau@mail.com"
#    modifier_employe(employe_a_modifier)

# Supprimer un employé
#supprimer_employe(1)

import unittest
import sys
import os

# Ajouter le chemin du projet au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.employe import Employe
from services.employe_service import ajouter_employe, recuperer_employe_par_id

class TestEmployeService(unittest.TestCase):
    def test_ajouter_employe(self):
        e = Employe(None, "Test", "User", "test.user@mail.com", 20, 1)
        ajouter_employe(e)
        employe_recupere = recuperer_employe_par_id(1)
        self.assertEqual(employe_recupere.nom, "Test")
        self.assertEqual(employe_recupere.prenom, "User")

if __name__ == "__main__":
    unittest.main()
