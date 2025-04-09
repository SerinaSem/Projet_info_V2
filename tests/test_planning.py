import unittest
from services.planning_service import generer_planning_semaine, afficher_planning_employe, generer_planning_optimise
from services.horaire_service import get_total_heures_employe
from models.employe import Employe

class TestPlanningService(unittest.TestCase):
    def test_generer_planning_semaine(self):
        try:
            generer_planning_semaine(1)
        except Exception as e:
            self.fail(f"Erreur lors de la génération du planning : {e}")

    def test_afficher_planning_employe(self):
        try:
            afficher_planning_employe(1)
        except Exception as e:
            self.fail(f"Erreur lors de l'affichage du planning employé : {e}")

    def test_generer_planning_optimise(self):
        try:
            generer_planning_optimise(1)
        except Exception as e:
            self.fail(f"Erreur lors de la génération du planning optimisé : {e}")

    def test_heures_assignation(self):
        generer_planning_semaine(1)
        employes = [Employe(1, "Durand", "Paul", "paul.durand@mail.com", 25, 1)]
        for employe in employes:
            heures_totales = get_total_heures_employe(employe.id)
            self.assertLessEqual(heures_totales, employe.contrat_heures, f"L'employé {employe.nom} dépasse ses heures de contrat.")

if __name__ == "__main__":
    unittest.main()
