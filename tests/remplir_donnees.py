import sys
import os
import bcrypt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.employe import Employe
from services.employe_service import ajouter_employe
from services.disponibilite_service import ajouter_disponibilites_semaine, ajouter_dispos_personnalisees
from services.besoin_service import ajouter_besoin
from models.besoin import Besoin

# === Génération des employés avec mot de passe "123" ===
base_employes = [
    ("Durand", "Emma", "emma.durand@mail.com", 25),
    ("Morel", "Lucas", "lucas.morel@mail.com", 30),
    ("Bernard", "Sophie", "sophie.bernard@mail.com", 35),
    ("Lemoine", "Alex", "alex.lemoine@mail.com", 20),
    ("Gomez", "Lea", "lea.gomez@mail.com", 25),
    ("Nguyen", "Hugo", "hugo.nguyen@mail.com", 35),
    ("Rossi", "Chloe", "chloe.rossi@mail.com", 30),
    ("Klein", "Tom", "tom.klein@mail.com", 20),
    ("Martin", "Julie", "julie.martin@mail.com", 25),
    ("Dupont", "Antoine", "antoine.dupont@mail.com", 28),
    ("Leroy", "Camille", "camille.leroy@mail.com", 32),
    ("Petit", "Nina", "nina.petit@mail.com", 24),
    ("Lopez", "Mathieu", "mathieu.lopez@mail.com", 30),
    ("Richard", "Anna", "anna.richard@mail.com", 26),
    ("Fontaine", "Yannis", "yannis.fontaine@mail.com", 27),
    ("Barbier", "Sami", "sami.barbier@mail.com", 22),
    ("Fabre", "Elise", "elise.fabre@mail.com", 34),
    ("David", "Lina", "lina.david@mail.com", 20)
]

hashed_password = bcrypt.hashpw("123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

for nom, prenom, email, contrat in base_employes:
    ajouter_employe(Employe(None, nom, prenom, email, contrat, 1, hashed_password)
)

# === Disponibilités réalistes ===
ajouter_disponibilites_semaine(1, "09:00", "17:00")
ajouter_dispos_personnalisees(2, {"Lundi": ("12:00", "20:00"), "Mercredi": ("10:00", "18:00")})
ajouter_disponibilites_semaine(3, "08:00", "16:00")
ajouter_disponibilites_semaine(4, "13:00", "21:00")
ajouter_disponibilites_semaine(5, "10:00", "18:00")
ajouter_disponibilites_semaine(6, "06:00", "14:00")
ajouter_dispos_personnalisees(7, {"Mardi": ("10:00", "18:00"), "Jeudi": ("14:00", "22:00")})
ajouter_disponibilites_semaine(8, "17:00", "23:00")
ajouter_disponibilites_semaine(9, "07:00", "15:00")
ajouter_disponibilites_semaine(10, "11:00", "19:00")
ajouter_disponibilites_semaine(11, "08:00", "16:00")
ajouter_dispos_personnalisees(12, {"Vendredi": ("09:00", "17:00"), "Dimanche": ("15:00", "23:00")})
ajouter_disponibilites_semaine(13, "10:00", "18:00")
ajouter_disponibilites_semaine(14, "12:00", "20:00")
ajouter_disponibilites_semaine(15, "05:00", "13:00")
ajouter_disponibilites_semaine(16, "15:00", "23:00")
ajouter_dispos_personnalisees(17, {"Samedi": ("11:00", "19:00"), "Dimanche": ("08:00", "16:00")})
ajouter_disponibilites_semaine(18, "09:00", "17:00")

# === Besoins du restaurant réalistes ===
jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
plages = [
    ("06:00", "10:00", 4),
    ("10:00", "14:00", 8),
    ("14:00", "18:00", 5),
    ("18:00", "22:00", 10),
    ("22:00", "01:00", 3)
]

for jour in jours:
    for debut, fin, nb in plages:
        ajouter_besoin(Besoin(None, 1, jour, debut, fin, nb))
