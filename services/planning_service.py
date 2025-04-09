from services.besoin_service import get_besoins_par_restaurant
from services.disponibilite_service import get_disponibilites_employe
from services.employe_service import recuperer_tous_employes
from services.horaire_service import ajouter_horaire
from models.horaire import Horaire
from datetime import datetime, timedelta
from services.horaire_service import get_total_heures_employe
from services.horaire_service import get_horaires_employe
from ortools.sat.python import cp_model


def afficher_donnees_disponibilites_et_besoins(id_restaurant):
    print(f"\n📋 Chargement des besoins pour le restaurant {id_restaurant}...\n")

    # Besoins du resto
    besoins = get_besoins_par_restaurant(id_restaurant)
    for b in besoins:
        print(f"🧑‍🍳 Besoin : {b.jour} de {b.heure_debut} à {b.heure_fin} → {b.nb_employes} employés")

    print("\n📋 Chargement des disponibilités des employés...\n")

    # Employés du resto
    employes = [e for e in recuperer_tous_employes() if e.id_restaurant == id_restaurant]
    for e in employes:
        print(f"👤 {e.nom} {e.prenom} (ID {e.id}) - Contrat : {e.contrat_heures}h/sem")
        dispos = get_disponibilites_employe(e.id)
        for d in dispos:
            print(f"   📆 {d.jour} de {d.heure_debut} à {d.heure_fin}")



def planning_simple_pour_jour(id_restaurant: int, jour_cible: str, heures_employes: dict, liste_employes: list):
    print(f"\n📆 Génération du planning pour le {jour_cible}...\n")

    besoins = [b for b in get_besoins_par_restaurant(id_restaurant) if b.jour == jour_cible]
    employes = [e for e in recuperer_tous_employes() if e.id_restaurant == id_restaurant]

    # Trier les employés par heures restantes (contrat_heures - heures_assignées)
    employes = sorted(employes, key=lambda e: e.contrat_heures - heures_employes[e.id])

    for besoin in besoins:
        nb_assignes = 0

        print(f"\n🧩 Besoin : {besoin.jour} {besoin.heure_debut}-{besoin.heure_fin} (x{besoin.nb_employes})")

        for employe in employes:
            heures_assignées = heures_employes[employe.id]
            print(f"   ➡️ Évaluation de l'employé {employe.nom} : {heures_assignées:.1f}h assignées / {employe.contrat_heures}h")

            dispos = get_disponibilites_employe(employe.id)

            # Prioriser les disponibilités qui correspondent aux préférences (si disponibles)
            dispos = sorted(dispos, key=lambda d: d.preference if hasattr(d, 'preference') else 0, reverse=True)

            for dispo in dispos:
                if dispo.jour == jour_cible:
                    print(f"      🔍 Disponibilité : {dispo.jour} de {dispo.heure_debut} à {dispo.heure_fin}")

                    # Vérifie si la dispo couvre le besoin
                    if dispo.heure_debut <= besoin.heure_debut and dispo.heure_fin >= besoin.heure_fin:
                        print(f"      ✅ La disponibilité couvre le besoin.")

                        # Calcul de la durée du besoin (en heures)
                        debut_besoin = datetime.strptime(besoin.heure_debut, "%H:%M")
                        fin_besoin = datetime.strptime(besoin.heure_fin, "%H:%M")
                        if fin_besoin < debut_besoin:  # Gérer les horaires qui passent à minuit
                            fin_besoin += timedelta(days=1)
                        duree_besoin = (fin_besoin - debut_besoin).total_seconds() / 3600

                        # Vérification des conflits avant l'assignation
                        if heures_assignées + duree_besoin > employe.contrat_heures:
                            print(f"      ❌ Conflit : {employe.nom} dépasserait son contrat ({heures_assignées + duree_besoin:.1f}h / {employe.contrat_heures}h).")
                            continue

                        # ✅ On peut l’assigner
                        h = Horaire(None, employe.id, jour_cible, besoin.heure_debut, besoin.heure_fin)
                        ajouter_horaire(h)
                        heures_employes[employe.id] += duree_besoin
                        print(f"      ✅ {employe.nom} assigné ({heures_employes[employe.id]:.1f}h / {employe.contrat_heures}h)")

                        nb_assignes += 1
                        break  # on ne prend qu’un créneau par employé
                    else:
                        print(f"      ❌ La disponibilité ne couvre pas le besoin.")

            if nb_assignes >= besoin.nb_employes:
                print(f"   ✅ Besoin rempli avec {nb_assignes}/{besoin.nb_employes} employés.")
                break  # besoin rempli
        else:
            print(f"   ❌ Besoin non entièrement couvert ({nb_assignes}/{besoin.nb_employes} employés assignés).")


def generer_planning_semaine(id_restaurant: int):
    jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    employes = [e for e in recuperer_tous_employes() if e.id_restaurant == id_restaurant]
    heures_employes = initialiser_heures_employes(employes)

    for jour in jours_semaine:
        print(f"\n📆 ====== {jour.upper()} ======")
        planning_simple_pour_jour(id_restaurant, jour, heures_employes, employes)

    print("\n✅ Génération complète du planning de la semaine terminée.")

#Affichage du planning hebdomadaire d’un employé
def afficher_planning_employe(id_employe: int):
    print(f"\n📅 Planning de l'employé ID {id_employe} :")
    horaires = get_horaires_employe(id_employe)
    
    if not horaires:
        print("Aucun horaire trouvé.")
        return

    horaires_triees = sorted(horaires, key=lambda h: h.jour)
    for h in horaires_triees:
        print(f"🕒 {h.jour} : {h.heure_debut} → {h.heure_fin}")


def initialiser_heures_employes(employes):
    return {e.id: get_total_heures_employe(e.id) for e in employes}

def generer_planning_optimise(id_restaurant: int):
    employes = [e for e in recuperer_tous_employes() if e.id_restaurant == id_restaurant]
    besoins = get_besoins_par_restaurant(id_restaurant)

    model = cp_model.CpModel()
    variables = {}
    heures_employes = {e.id: get_total_heures_employe(e.id) for e in employes}

    for besoin in besoins:
        for employe in employes:
            dispo = any(
                d.jour == besoin.jour and d.heure_debut <= besoin.heure_debut and d.heure_fin >= besoin.heure_fin
                for d in get_disponibilites_employe(employe.id)
            )
            if dispo:
                var_name = f"x_{employe.id}_{besoin.id}"
                variables[var_name] = model.NewBoolVar(var_name)

    # Contraintes : chaque besoin doit être couvert
    for besoin in besoins:
        model.Add(
            sum(variables[f"x_{e.id}_{besoin.id}"] for e in employes if f"x_{e.id}_{besoin.id}" in variables) == besoin.nb_employes
        )

    # Contraintes : respecter les heures de contrat
    for employe in employes:
        heures_totales = sum(
            variables[f"x_{employe.id}_{b.id}"] * (datetime.strptime(b.heure_fin, "%H:%M") - datetime.strptime(b.heure_debut, "%H:%M")).seconds / 3600
            for b in besoins if f"x_{employe.id}_{b.id}" in variables
        )
        model.Add(heures_totales + heures_employes[employe.id] <= employe.contrat_heures)

    # Fonction objectif : minimiser les heures non assignées
    model.Maximize(
        sum(variables[var] for var in variables)
    )

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for var_name, var in variables.items():
            if solver.Value(var):
                _, employe_id, besoin_id = var_name.split("_")
                besoin = next(b for b in besoins if b.id == int(besoin_id))
                ajouter_horaire(Horaire(None, int(employe_id), besoin.jour, besoin.heure_debut, besoin.heure_fin))
    else:
        print("❌ Aucun planning optimal trouvé.")
