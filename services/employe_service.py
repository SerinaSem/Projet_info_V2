import sqlite3
from models.employe import Employe

DB_PATH = "planning_resto.db"

# 🔹 Ajouter un employé
def ajouter_employe(employe: Employe):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO employe (nom, prenom, email, contrat_heures, id_restaurant)
        VALUES (?, ?, ?, ?, ?)
    """, (employe.nom, employe.prenom, employe.email, employe.contrat_heures, employe.id_restaurant))
    conn.commit()
    conn.close()
    print(f"✅ Employé {employe.nom} ajouté avec succès.")

# 🔹 Récupérer tous les employés
def recuperer_tous_employes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employe")
    rows = cursor.fetchall()
    conn.close()
    return [Employe(*row) for row in rows]

# 🔹 Récupérer un employé par ID
def recuperer_employe_par_id(id_employe):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employe WHERE id = ?", (id_employe,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Employe(*row)
    else:
        print("❌ Aucun employé trouvé avec cet ID.")
        return None

# 🔹 Modifier un employé
def modifier_employe(employe: Employe):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employe
        SET nom = ?, prenom = ?, email = ?, contrat_heures = ?, id_restaurant = ?
        WHERE id = ?
    """, (employe.nom, employe.prenom, employe.email, employe.contrat_heures, employe.id_restaurant, employe.id))
    conn.commit()
    conn.close()
    print(f"✏️ Employé {employe.id} modifié avec succès.")

# 🔹 Supprimer un employé
def supprimer_employe(id_employe):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employe WHERE id = ?", (id_employe,))
    conn.commit()
    conn.close()
    print(f"🗑️ Employé {id_employe} supprimé avec succès.")
