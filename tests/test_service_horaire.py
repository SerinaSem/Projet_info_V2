from models.horaire import Horaire
from services.horaire_service import *

# Ajouter un horaire
h1 = Horaire(None, 2, "2025-04-09", "09:00", "13:00")
ajouter_horaire(h1)

# Récupérer les horaires de l'employé 2
horaires = get_horaires_employe(2)
for h in horaires:
    print(f"{h.jour} de {h.heure_debut} à {h.heure_fin}")

# Supprimer un horaire
supprimer_horaire(h1.id)  # (ou via une variable récupérée)
