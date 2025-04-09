import sqlite3
from models.besoin import Besoin

DB_PATH = "planning_resto.db"

# 🔹 Ajouter un besoin
def ajouter_besoin(besoin: Besoin):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO besoin (id_restaurant, jour, heure_debut, heure_fin, nb_employes)
        VALUES (?, ?, ?, ?, ?)
    """, (besoin.id_restaurant, besoin.jour, besoin.heure_debut, besoin.heure_fin, besoin.nb_employes))
    conn.commit()
    conn.close()
    print(f"✅ Besoin ajouté pour le restaurant ID {besoin.id_restaurant}")

# 🔹 Récupérer les besoins d’un restaurant
def get_besoins_par_restaurant(id_restaurant):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM besoin WHERE id_restaurant = ?
    """, (id_restaurant,))
    rows = cursor.fetchall()
    conn.close()
    return [Besoin(*row) for row in rows]

# 🔹 Supprimer un besoin par ID
def supprimer_besoin(id_besoin):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM besoin WHERE id = ?", (id_besoin,))
    conn.commit()
    conn.close()
    print(f"🗑️ Besoin ID {id_besoin} supprimé.")

# (Optionnel) 🔹 Modifier un besoin
def modifier_besoin(besoin: Besoin):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE besoin
        SET jour = ?, heure_debut = ?, heure_fin = ?, nb_employes = ?
        WHERE id = ?
    """, (besoin.jour, besoin.heure_debut, besoin.heure_fin, besoin.nb_employes, besoin.id))
    conn.commit()
    conn.close()
    print(f"✏️ Besoin ID {besoin.id} modifié.")
