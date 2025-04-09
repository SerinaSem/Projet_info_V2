from services.planning_service import afficher_donnees_disponibilites_et_besoins
from services.planning_service import planning_simple_pour_jour
from services.planning_service import generer_planning_semaine

# On teste pour le restaurant ID 1
#afficher_donnees_disponibilites_et_besoins(1)

#planning_simple_pour_jour(1, "Lundi")


# Générer tout le planning de la semaine
generer_planning_semaine(1)


from services.planning_service import afficher_planning_employe

#afficher_planning_employe(1)
#afficher_planning_employe(2)


