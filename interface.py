import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import Calendar
from models.employe import Employe
from services.planning_service import generer_planning_semaine, afficher_planning_employe
from services.employe_service import ajouter_employe, recuperer_tous_employes
from services.horaire_service import get_tous_les_horaires  # Import the required function
from PIL import Image, ImageTk  # Import for handling images
import os  # Import for checking file existence

class PlanningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Plannings - Restaurant")
        self.root.geometry("1000x700")

        # Création des onglets
        self.tab_control = ttk.Notebook(self.root)
        self.tab_employes = ttk.Frame(self.tab_control)
        self.tab_disponibilites = ttk.Frame(self.tab_control)
        self.tab_besoins = ttk.Frame(self.tab_control)
        self.tab_plannings = ttk.Frame(self.tab_control)
        self.tab_planning_employes = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_employes, text="Employés")
        self.tab_control.add(self.tab_disponibilites, text="Disponibilités")
        self.tab_control.add(self.tab_besoins, text="Besoins")
        self.tab_control.add(self.tab_plannings, text="Plannings")
        self.tab_control.add(self.tab_planning_employes, text="Planning Employés")
        self.tab_control.pack(expand=1, fill="both")

        # Initialisation des sections
        self.create_employes_tab()
        self.create_disponibilites_tab()
        self.create_besoins_tab()
        self.create_plannings_tab()
        self.create_planning_employes_tab()
        self.create_parametres_tab()

    def create_employes_tab(self):
        tk.Label(self.tab_employes, text="Gestion des Employés", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

        # Employee table with an image column
        self.tree_employes = ttk.Treeview(
            self.tab_employes, 
            columns=("Image", "Nom", "Prénom", "Email", "Contrat"), 
            show="headings", 
            height=15
        )
        self.tree_employes.heading("Image", text="Photo")
        self.tree_employes.heading("Nom", text="Nom")
        self.tree_employes.heading("Prénom", text="Prénom")
        self.tree_employes.heading("Email", text="Email")
        self.tree_employes.heading("Contrat", text="Heures Contrat")
        self.tree_employes.column("Image", width=50)  # Adjust image column width
        self.tree_employes.pack(expand=True, fill="both", pady=10)

        # Action buttons with icons
        frame_buttons = tk.Frame(self.tab_employes, bg="#f0f0f0")
        frame_buttons.pack(pady=10)

        # Load icons for buttons with fallback to text-only buttons
        try:
            add_icon = ImageTk.PhotoImage(Image.open("icons/add.png").resize((20, 20))) if os.path.exists("icons/add.png") else None
            edit_icon = ImageTk.PhotoImage(Image.open("icons/edit.png").resize((20, 20))) if os.path.exists("icons/edit.png") else None
            delete_icon = ImageTk.PhotoImage(Image.open("icons/delete.png").resize((20, 20))) if os.path.exists("icons/delete.png") else None
        except Exception as e:
            add_icon = edit_icon = delete_icon = None
            print(f"Error loading icons: {e}")

        tk.Button(frame_buttons, text=" Ajouter Employé", image=add_icon, compound="left" if add_icon else None, command=self.ajouter_employe).grid(row=0, column=0, padx=5)
        tk.Button(frame_buttons, text=" Modifier Employé", image=edit_icon, compound="left" if edit_icon else None, command=self.modifier_employe).grid(row=0, column=1, padx=5)
        tk.Button(frame_buttons, text=" Supprimer Employé", image=delete_icon, compound="left" if delete_icon else None, command=self.supprimer_employe).grid(row=0, column=2, padx=5)

        # Keep references to icons to prevent garbage collection
        self.add_icon = add_icon
        self.edit_icon = edit_icon
        self.delete_icon = delete_icon

        self.afficher_employes()  # Load employees on startup

    def create_disponibilites_tab(self):
        tk.Label(self.tab_disponibilites, text="Gestion des Disponibilités", font=("Arial", 16)).pack(pady=10)
        
        # Formulaire pour ajouter une disponibilité
        frame_form = tk.Frame(self.tab_disponibilites)
        frame_form.pack(pady=10)
        
        tk.Label(frame_form, text="Jour:").grid(row=0, column=0)
        entry_jour = tk.Entry(frame_form)
        entry_jour.grid(row=0, column=1)
        
        tk.Label(frame_form, text="Heure Début:").grid(row=1, column=0)
        entry_heure_debut = tk.Entry(frame_form)
        entry_heure_debut.grid(row=1, column=1)
        
        tk.Label(frame_form, text="Heure Fin:").grid(row=2, column=0)
        entry_heure_fin = tk.Entry(frame_form)
        entry_heure_fin.grid(row=2, column=1)
        
        tk.Button(frame_form, text="Ajouter Disponibilité", command=lambda: self.ajouter_disponibilite(entry_jour.get(), entry_heure_debut.get(), entry_heure_fin.get())).grid(row=3, column=0, columnspan=2)
        
        # Zone d'affichage des disponibilités
        self.text_disponibilites = tk.Text(self.tab_disponibilites, wrap=tk.WORD, height=20, width=80)
        self.text_disponibilites.pack(pady=10)

    def ajouter_disponibilite(self, jour, heure_debut, heure_fin):
        try:
            # Logique pour ajouter une disponibilité (à implémenter dans le service)
            messagebox.showinfo("Succès", f"Disponibilité ajoutée : {jour} {heure_debut}-{heure_fin}")
            self.afficher_disponibilites()  # Rafraîchir l'affichage
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout de la disponibilité : {e}")

    def create_besoins_tab(self):
        tk.Label(self.tab_besoins, text="Gestion des Besoins", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.tab_besoins, text="Afficher Besoins", command=self.afficher_besoins).pack(pady=5)
        self.text_besoins = tk.Text(self.tab_besoins, wrap=tk.WORD, height=20, width=80)
        self.text_besoins.pack(pady=10)

    def create_plannings_tab(self):
        tk.Label(self.tab_plannings, text="Gestion des Plannings", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.tab_plannings, text="Générer Planning", command=self.generer_planning).pack(pady=5)
        tk.Button(self.tab_plannings, text="Afficher Planning Employé", command=self.afficher_planning_employe).pack(pady=5)
        tk.Button(self.tab_plannings, text="Calendrier", command=self.afficher_calendrier).pack(pady=5)
        self.text_plannings = tk.Text(self.tab_plannings, wrap=tk.WORD, height=20, width=80)
        self.text_plannings.pack(pady=10)

    def create_planning_employes_tab(self):
        tk.Label(self.tab_planning_employes, text="Planning des Employés", font=("Arial", 16)).pack(pady=10)
        
        # Création du tableau
        self.tree_planning = ttk.Treeview(self.tab_planning_employes, columns=("Jour", "Heure", "Tâche"), show="headings")
        self.tree_planning.heading("Jour", text="Jour")
        self.tree_planning.heading("Heure", text="Heure")
        self.tree_planning.heading("Tâche", text="Tâche")
        self.tree_planning.pack(expand=True, fill="both", pady=10)

        # Bouton pour charger les plannings
        tk.Button(self.tab_planning_employes, text="Charger Planning", command=self.afficher_planning_employes).pack(pady=5)

    def create_parametres_tab(self):
        self.tab_parametres = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_parametres, text="Paramètres")
        
        tk.Label(self.tab_parametres, text="Paramètres", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.tab_parametres, text="Heures d'ouverture:").pack(pady=5)
        entry_heures_ouverture = tk.Entry(self.tab_parametres)
        entry_heures_ouverture.pack(pady=5)
        tk.Button(self.tab_parametres, text="Enregistrer", command=lambda: self.enregistrer_parametres(entry_heures_ouverture.get())).pack(pady=5)

    def enregistrer_parametres(self, heures_ouverture):
        try:
            # Logique pour enregistrer les paramètres
            messagebox.showinfo("Succès", "Paramètres enregistrés avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement des paramètres : {e}")

    def ajouter_employe(self):
        def save_employe():
            nom = entry_nom.get()
            prenom = entry_prenom.get()
            email = entry_email.get()
            contrat = int(entry_contrat.get())
            ajouter_employe(Employe(None, nom, prenom, email, contrat, 1))
            messagebox.showinfo("Succès", "Employé ajouté avec succès.")
            add_window.destroy()
            self.afficher_employes()  # Rafraîchir la liste des employés

        add_window = tk.Toplevel(self.root)
        add_window.title("Ajouter un Employé")
        tk.Label(add_window, text="Nom:").grid(row=0, column=0)
        entry_nom = tk.Entry(add_window)
        entry_nom.grid(row=0, column=1)
        tk.Label(add_window, text="Prénom:").grid(row=1, column=0)
        entry_prenom = tk.Entry(add_window)
        entry_prenom.grid(row=1, column=1)
        tk.Label(add_window, text="Email:").grid(row=2, column=0)
        entry_email = tk.Entry(add_window)
        entry_email.grid(row=2, column=1)
        tk.Label(add_window, text="Heures Contrat:").grid(row=3, column=0)
        entry_contrat = tk.Entry(add_window)
        entry_contrat.grid(row=3, column=1)
        tk.Button(add_window, text="Enregistrer", command=save_employe).grid(row=4, column=0, columnspan=2)

    def modifier_employe(self):
        selected_item = self.tree_employes.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un employé à modifier.")
            return

        # Récupérer les données de l'employé sélectionné
        employe_data = self.tree_employes.item(selected_item)["values"]
        if not employe_data:
            messagebox.showerror("Erreur", "Impossible de récupérer les données de l'employé.")
            return

        # Ouvrir une fenêtre pour modifier les informations
        def save_modifications():
            nom = entry_nom.get()
            prenom = entry_prenom.get()
            email = entry_email.get()
            contrat = int(entry_contrat.get())

            # Appeler le service pour mettre à jour l'employé
            try:
                from services.employe_service import modifier_employe
                employe = Employe(employe_data[0], nom, prenom, email, contrat, 1)
                modifier_employe(employe)
                messagebox.showinfo("Succès", "Employé modifié avec succès.")
                self.afficher_employes()  # Rafraîchir la liste des employés
                edit_window.destroy()  # Fermer la fenêtre de modification
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la modification : {e}")

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Modifier un Employé")

        tk.Label(edit_window, text="Nom:").grid(row=0, column=0)
        entry_nom = tk.Entry(edit_window)
        entry_nom.insert(0, employe_data[0])  # Pré-remplir avec le nom actuel
        entry_nom.grid(row=0, column=1)

        tk.Label(edit_window, text="Prénom:").grid(row=1, column=0)
        entry_prenom = tk.Entry(edit_window)
        entry_prenom.insert(0, employe_data[1])  # Pré-remplir avec le prénom actuel
        entry_prenom.grid(row=1, column=1)

        tk.Label(edit_window, text="Email:").grid(row=2, column=0)
        entry_email = tk.Entry(edit_window)
        entry_email.insert(0, employe_data[2])  # Pré-remplir avec l'email actuel
        entry_email.grid(row=2, column=1)

        tk.Label(edit_window, text="Heures Contrat:").grid(row=3, column=0)
        entry_contrat = tk.Entry(edit_window)
        entry_contrat.insert(0, employe_data[3])  # Pré-remplir avec les heures de contrat actuelles
        entry_contrat.grid(row=3, column=1)

        tk.Button(edit_window, text="Enregistrer", command=save_modifications).grid(row=4, column=0, columnspan=2)

    def supprimer_employe(self):
        selected_item = self.tree_employes.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un employé à supprimer.")
            return
        
        employe_data = self.tree_employes.item(selected_item)["values"]
        if not employe_data:
            messagebox.showerror("Erreur", "Impossible de récupérer les données de l'employé.")
            return

        try:
            from services.employe_service import supprimer_employe
            supprimer_employe(employe_data[0])  # employe_data[0] = ID
            messagebox.showinfo("Succès", "Employé supprimé avec succès.")
            self.afficher_employes()  # Rafraîchir la liste des employés
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}")

    def afficher_calendrier(self):
        cal_window = tk.Toplevel(self.root)
        cal_window.title("Calendrier des Plannings")
        cal = Calendar(cal_window, selectmode="day", year=2025, month=4, day=7)
        cal.pack(pady=20)
        tk.Button(cal_window, text="Afficher Planning", command=lambda: self.afficher_planning_date(cal.get_date())).pack()

    def afficher_planning_date(self, date):
        # Logique pour afficher le planning du jour sélectionné
        messagebox.showinfo("Planning", f"Planning pour le {date}")

    def afficher_employes(self):
        employes = recuperer_tous_employes()
        for row in self.tree_employes.get_children():
            self.tree_employes.delete(row)

        colors = ["#f9f9f9", "#e6f7ff"]  # Alternating row colors
        for index, employe in enumerate(employes):
            color = colors[index % len(colors)]
            self.tree_employes.insert(
                "", tk.END, 
                values=("", employe.nom, employe.prenom, employe.email, getattr(employe, 'contrat', 'N/A')),
                tags=(color,)
            )
        for color in colors:
            self.tree_employes.tag_configure(color, background=color)

    def afficher_disponibilites(self):
        self.text_disponibilites.delete(1.0, tk.END)
        try:
            # Replace the following line with the actual logic to fetch availabilities
            disponibilites = ["Lundi 09:00-17:00", "Mardi 10:00-18:00"]  # Example data
            for dispo in disponibilites:
                self.text_disponibilites.insert(tk.END, f"{dispo}\n")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage des disponibilités : {e}")

    def afficher_besoins(self):
        self.text_besoins.delete(1.0, tk.END)
        try:
            # Replace the following line with the actual logic to fetch needs
            besoins = ["Lundi 09:00-12:00 - 2 employés", "Mardi 14:00-18:00 - 3 employés"]  # Example data
            for besoin in besoins:
                self.text_besoins.insert(tk.END, f"{besoin}\n")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage des besoins : {e}")

    def generer_planning(self):
        try:
            generer_planning_semaine(1)  # ID du restaurant
            messagebox.showinfo("Succès", "Planning généré avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération du planning : {e}")

    def afficher_planning_employe(self):
        self.text_plannings.delete(1.0, tk.END)
        try:
            id_employe = int(self.prompt_user("Entrez l'ID de l'employé :"))
            planning = afficher_planning_employe(id_employe)
            self.text_plannings.insert(tk.END, f"Planning de l'employé ID {id_employe} :\n{planning}\n")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un ID valide.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur : {e}")

    def afficher_planning_employes(self):
        # Vider le tableau avant d'ajouter de nouvelles données
        for row in self.tree_planning.get_children():
            self.tree_planning.delete(row)

        try:
            # Récupérer les plannings depuis la base de données
            plannings = get_tous_les_horaires()

            # Ajouter les données au tableau
            for planning in plannings:
                self.tree_planning.insert(
                    "", tk.END, 
                    values=(planning.jour, f"{planning.heure_debut}-{planning.heure_fin}", f"Employé ID {planning.id_employe}")
                )
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des plannings : {e}")

    def prompt_user(self, message):
        return simpledialog.askstring("Input", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlanningApp(root)
    root.mainloop()
