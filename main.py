import tkinter as tk
from tkinter import messagebox
from services.employe_service import recuperer_employe_par_id
from interface import PlanningApp

# ==== Interface Employé Simplifiée ====
class EmployeView:
    def __init__(self, root, employe_id):
        self.root = root
        self.root.title("Planning Employé")
        self.root.geometry("600x400")

        from services.planning_service import get_horaires_employe
        horaires = get_horaires_employe(employe_id)

        tk.Label(root, text=f"👋 Bienvenue Employé #{employe_id}", font=("Arial", 16, "bold"), pady=10).pack()

        frame = tk.Frame(root)
        frame.pack(pady=10)

        if horaires:
            for h in sorted(horaires, key=lambda h: h.jour):
                txt = f"{h.jour} : {h.heure_debut} → {h.heure_fin}"
                tk.Label(frame, text=txt, font=("Arial", 12)).pack()
        else:
            tk.Label(frame, text="Aucun horaire assigné cette semaine.", font=("Arial", 12), fg="gray").pack()


# ==== Fenêtre de Connexion ====
class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connexion au Planning")
        self.root.geometry("450x300")
        self.root.configure(bg="#f5f5f5")

        tk.Label(self.root, text="🍽️ Bienvenue dans le Gestionnaire de Planning", font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=10)
        tk.Label(self.root, text="Merci de vous connecter pour continuer", font=("Arial", 11), bg="#f5f5f5").pack(pady=5)

        tk.Label(self.root, text="Identifiant Employé :", font=("Arial", 11), bg="#f5f5f5").pack(pady=10)
        self.entry_id = tk.Entry(self.root, font=("Arial", 12))
        self.entry_id.pack(pady=5)

        tk.Button(self.root, text="👤 Se connecter comme Employé", font=("Arial", 11), command=self.lancer_employe, bg="#d0eaff").pack(pady=5)
        tk.Button(self.root, text="🧑‍💼 Se connecter comme Employeur", font=("Arial", 11), command=self.lancer_employeur, bg="#ffd9b3").pack(pady=5)

        self.root.mainloop()

    def lancer_employe(self):
        try:
            id_employe = int(self.entry_id.get())
            employe = recuperer_employe_par_id(id_employe)
            if employe:
                self.root.destroy()
                root = tk.Tk()
                EmployeView(root, id_employe)
                root.mainloop()
            else:
                messagebox.showerror("Erreur", "Employé non trouvé.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un identifiant valide.")

    def lancer_employeur(self):
        self.root.destroy()
        root = tk.Tk()
        PlanningApp(root)
        root.mainloop()


# ==== Point d'entrée ==== 
if __name__ == "__main__":
    LoginWindow()