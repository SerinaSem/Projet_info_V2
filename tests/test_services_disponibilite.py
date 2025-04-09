from models.disponibilite import Disponibilite
from services.disponibilite_service import *

# Ajouter une disponibilité
dispos_custom = {
    "Lundi": ("09:00", "13:00"),
    "Mardi": ("14:00", "18:00"),
    "Mercredi": ("08:00", "12:00"),
    "Jeudi": ("10:00", "15:00"),
    "Vendredi": ("08:00", "15:00")
}

ajouter_dispos_personnalisees(3, dispos_custom)



# Lire les dispos de l'employé 1
#dispos = get_disponibilites_employe(1)
#for d in dispos:
#    print(f"{d.jour} de {d.heure_debut} à {d.heure_fin}")


# Modifier une dispo
#d_modif = dispos[0]
#d_modif.heure_debut = "12:00"
#d_modif.heure_fin = "15:00"
#modifier_disponibilite(d_modif)

# Supprimer une dispo
#supprimer_disponibilite(5)
#supprimer_disponibilite(6)
