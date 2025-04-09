class Employe:
    def __init__(self, id, nom, prenom, email, contrat_heures, id_restaurant):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.contrat_heures = contrat_heures
        self.id_restaurant = id_restaurant

    def __repr__(self):
        return f"<Employe {self.nom} {self.prenom} (ID: {self.id})>"
