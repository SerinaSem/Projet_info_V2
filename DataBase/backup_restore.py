import os

# Fonction pour sauvegarder la base de données
def sauvegarder_base():
    try:
        os.system("pg_dump -U your_username -F c -b -v -f backup_file.dump planning_resto")
        print("✅ Sauvegarde effectuée avec succès.")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")

# Fonction pour restaurer la base de données
def restaurer_base():
    try:
        os.system("pg_restore -U your_username -d planning_resto -v backup_file.dump")
        print("✅ Restauration effectuée avec succès.")
    except Exception as e:
        print(f"❌ Erreur lors de la restauration : {e}")

if __name__ == "__main__":
    print("1. Sauvegarder la base de données")
    print("2. Restaurer la base de données")
    choix = input("Choisissez une option (1 ou 2) : ")

    if choix == "1":
        sauvegarder_base()
    elif choix == "2":
        restaurer_base()
    else:
        print("❌ Option invalide.")
