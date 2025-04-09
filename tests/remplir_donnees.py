import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.employe import Employe
from services.employe_service import ajouter_employe
from services.disponibilite_service import ajouter_disponibilites_semaine, ajouter_dispos_personnalisees
from services.besoin_service import ajouter_besoin
from models.besoin import Besoin


employes = [
    ("Durand", "Emma", "emma.durand@mail.com", 25),
    ("Morel", "Lucas", "lucas.morel@mail.com", 30),
    ("Bernard", "Sophie", "sophie.bernard@mail.com", 35),
    ("Lemoine", "Alex", "alex.lemoine@mail.com", 20),
    ("Gomez", "Lea", "lea.gomez@mail.com", 25),
    ("Nguyen", "Hugo", "hugo.nguyen@mail.com", 35),
    ("Rossi", "Chloe", "chloe.rossi@mail.com", 30),
    ("Klein", "Tom", "tom.klein@mail.com", 20)
]

for nom, prenom, email, contrat in employes:
    ajouter_employe(Employe(None, nom, prenom, email, contrat, 1))



# Chaque employé travaille 2 à 3 jours, horaires réalistes
ajouter_disponibilites_semaine(1, "09:00", "17:00")  # Employé 1
ajouter_disponibilites_semaine(2, "08:00", "16:00")  # Employé 2
ajouter_disponibilites_semaine(3, "12:00", "20:00")  # Employé 3
ajouter_dispos_personnalisees(2, {
    "Lundi": ("11:00", "19:00"),
    "Mercredi": ("06:00", "14:00"),
    "Samedi": ("10:00", "18:00")
})
ajouter_disponibilites_semaine(3, "05:00", "13:00")  # Sophie
ajouter_disponibilites_semaine(4, "12:00", "20:00")  # Alex
ajouter_disponibilites_semaine(5, "08:00", "16:00")  # Lea
ajouter_dispos_personnalisees(6, {
    "Mardi": ("10:00", "18:00"),
    "Jeudi": ("11:00", "15:00"),
    "Dimanche": ("14:00", "22:00")
})
ajouter_disponibilites_semaine(7, "09:00", "17:00")
ajouter_disponibilites_semaine(8, "18:00", "00:00")


jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# Heures de service
plages = [
    ("05:00", "11:00", 6),
    ("11:00", "15:00", 10),  # Rush
    ("15:00", "18:00", 6),
    ("18:00", "21:00", 10),  # Rush
    ("21:00", "00:00", 6)
]

for jour in jours:
    for debut, fin, nb in plages:
        ajouter_besoin(Besoin(None, 1, jour, debut, fin, nb))
