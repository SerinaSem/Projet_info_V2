from models.besoin import Besoin
from services.besoin_service import *

# Ajouter un besoin
b1 = Besoin(None, 1, "Lundi", "12:00", "13:00", 3)
ajouter_besoin(b1)

# Lire les besoins du restaurant 1
#besoins = get_besoins_par_restaurant(1)
#for b in besoins:
#    print(f"{b.jour} de {b.heure_debut} à {b.heure_fin} - {b.nb_employes} employés")

# Modifier un besoin
#b_modif = besoins[0]
#b_modif.nb_employes = 1
#modifier_besoin(b_modif)

# Supprimer un besoin
#supprimer_besoin(4)
