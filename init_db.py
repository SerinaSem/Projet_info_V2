from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# Définition des modèles
class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    adresse = Column(String)

class Employe(Base):
    __tablename__ = 'employe'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String)
    mot_de_passe = Column(String)
    contrat_heures = Column(Integer, nullable=False)
    id_restaurant = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship("Restaurant", back_populates="employes")

class Disponibilite(Base):
    __tablename__ = 'disponibilite'
    id = Column(Integer, primary_key=True)
    id_employe = Column(Integer, ForeignKey('employe.id'))
    jour = Column(String)
    heure_debut = Column(String)
    heure_fin = Column(String)

class Besoin(Base):
    __tablename__ = 'besoin'
    id = Column(Integer, primary_key=True)
    id_restaurant = Column(Integer, ForeignKey('restaurant.id'))
    jour = Column(String)
    heure_debut = Column(String)
    heure_fin = Column(String)
    nb_employes = Column(Integer)

class Horaire(Base):
    __tablename__ = 'horaire'
    id = Column(Integer, primary_key=True)
    id_employe = Column(Integer, ForeignKey('employe.id'))
    jour = Column(String)
    heure_debut = Column(String)
    heure_fin = Column(String)

Restaurant.employes = relationship("Employe", order_by=Employe.id, back_populates="restaurant")

# Configuration de la base de données
DATABASE_URL = "postgresql://your_username:your_password@localhost/planning_resto"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création des tables
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données initialisée avec SQLAlchemy.")
