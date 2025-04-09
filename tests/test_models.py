import unittest
import sys
import os

# Ajouter le chemin du projet au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.employe import Employe
from models.disponibilite import Disponibilite

class TestEmployeModel(unittest.TestCase):
    def test_employe_creation(self):
        e = Employe(1, "Durand", "Paul", "paul.durand@mail.com", 35, 1)
        self.assertEqual(e.nom, "Durand")
        self.assertEqual(e.prenom, "Paul")
        self.assertEqual(e.email, "paul.durand@mail.com")
        self.assertEqual(e.contrat_heures, 35)
        self.assertEqual(e.id_restaurant, 1)

class TestDisponibiliteModel(unittest.TestCase):
    def test_disponibilite_creation(self):
        d = Disponibilite(1, 1, "Lundi", "09:00", "17:00")
        self.assertEqual(d.id, 1)
        self.assertEqual(d.id_employe, 1)
        self.assertEqual(d.jour, "Lundi")
        self.assertEqual(d.heure_debut, "09:00")
        self.assertEqual(d.heure_fin, "17:00")

if __name__ == "__main__":
    unittest.main()
