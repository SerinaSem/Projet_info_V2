import sqlite3
from models.disponibilite import Disponibilite

DB_PATH = "planning_resto.db"

# 🔹 Ajouter une disponibilité
def ajouter_disponibilite(dispo: Disponibilite):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO disponibilite (id_employe, jour, heure_debut, heure_fin)
        VALUES (?, ?, ?, ?)
    """, (dispo.id_employe, dispo.jour, dispo.heure_debut, dispo.heure_fin))
    conn.commit()
    conn.close()
    print(f"✅ Disponibilité ajoutée pour l'employé ID {dispo.id_employe}")

# 🔹 Récupérer les disponibilités d’un employé
def get_disponibilites_employe(id_employe):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM disponibilite WHERE id_employe = ?
    """, (id_employe,))
    rows = cursor.fetchall()
    conn.close()
    return [Disponibilite(*row) for row in rows]

# 🔹 Supprimer une disponibilité par ID
def supprimer_disponibilite(id_dispo):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM disponibilite WHERE id = ?", (id_dispo,))
    conn.commit()
    conn.close()
    print(f"🗑️ Disponibilité ID {id_dispo} supprimée.")

# (Optionnel) 🔹 Modifier une disponibilité
def modifier_disponibilite(dispo: Disponibilite):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE disponibilite
        SET jour = ?, heure_debut = ?, heure_fin = ?
        WHERE id = ?
    """, (dispo.jour, dispo.heure_debut, dispo.heure_fin, dispo.id))
    conn.commit()
    conn.close()
    print(f"✏️ Disponibilité ID {dispo.id} modifiée.")

def ajouter_dispos_personnalisees(id_employe: int, horaires_par_jour: dict):
    """
    horaires_par_jour = {
        "Lundi": ("10:00", "14:00"),
        "Mardi": ("12:00", "16:00"),
        "Jeudi": ("09:00", "13:00"),
        ...
    }
    """
    for jour, (heure_debut, heure_fin) in horaires_par_jour.items():
        dispo = Disponibilite(None, id_employe, jour, heure_debut, heure_fin)
        ajouter_disponibilite(dispo)

    print(f"✅ Disponibilités personnalisées ajoutées pour l'employé ID {id_employe}")


def ajouter_disponibilites_semaine(id_employe: int, heure_debut: str, heure_fin: str):
    jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    for jour in jours_semaine:
        dispo = Disponibilite(None, id_employe, jour, heure_debut, heure_fin)
        ajouter_disponibilite(dispo)
    print(f"✅ Dispos semaine ajoutées pour employé {id_employe}")
