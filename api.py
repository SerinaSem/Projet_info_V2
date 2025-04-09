from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from init_db import Base, Employe, Horaire, Besoin
from sqlalchemy.exc import NoResultFound
import bcrypt

app = Flask(__name__)
CORS(app)

# ===== CONFIG DB =====
DB_PATH = "sqlite:///planning_resto.db"
engine = create_engine(DB_PATH)
SessionLocal = sessionmaker(bind=engine)

# ===== UTILS =====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===== ROUTES =====

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    role = data.get('role')

    if role == 'employeur':
        # Vérification du code employeur
        code = data.get('code')
        if code == '123456789':
            return jsonify({"success": True, "employeur": True})
        else:
            return jsonify({"success": False, "message": "Code employeur incorrect."})

    # Sinon on fait la connexion normale employé
    email = data.get("email")
    mot_de_passe = data.get("mot_de_passe")

    session = SessionLocal()
    try:
        employe = session.query(Employe).filter_by(email=email).first()
        if employe and bcrypt.checkpw(mot_de_passe.encode(), employe.mot_de_passe.encode()):
            return jsonify({
                "success": True,
                "employe": {
                    "id": employe.id,
                    "nom": employe.nom,
                    "prenom": employe.prenom,
                    "email": employe.email,
                    "id_restaurant": employe.id_restaurant
                }
            })
        else:
            return jsonify({"success": False, "message": "Email ou mot de passe incorrect."})
    finally:
        session.close()



@app.route("/planning/<int:id_employe>", methods=["GET"])
def get_planning_employe(id_employe):
    session = SessionLocal()
    try:
        horaires = session.query(Horaire).filter_by(id_employe=id_employe).all()
        return jsonify([{
            "jour": h.jour,
            "heure_debut": h.heure_debut,
            "heure_fin": h.heure_fin
        } for h in horaires])
    finally:
        session.close()


@app.route("/employes", methods=["GET"])
def get_employes():
    session = SessionLocal()
    try:
        employes = session.query(Employe).all()
        return jsonify([{
            "id": e.id,
            "nom": e.nom,
            "prenom": e.prenom,
            "email": e.email,
            "contrat_heures": e.contrat_heures
        } for e in employes])
    finally:
        session.close()


@app.route("/employes", methods=["POST"])
def ajouter_employe():
    data = request.get_json()
    session = SessionLocal()
    try:
        mot_de_passe_hash = bcrypt.hashpw(data["mot_de_passe"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        nouvel_employe = Employe(
            nom=data["nom"],
            prenom=data["prenom"],
            email=data["email"],
            mot_de_passe=mot_de_passe_hash,
            contrat_heures=data["contrat_heures"],
            id_restaurant=data["id_restaurant"]
        )
        session.add(nouvel_employe)
        session.commit()
        return jsonify({"success": True, "id": nouvel_employe.id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        session.close()


@app.route("/besoins", methods=["GET"])
def get_besoins():
    session = SessionLocal()
    try:
        besoins = session.query(Besoin).all()
        return jsonify([{
            "jour": b.jour,
            "heure_debut": b.heure_debut,
            "heure_fin": b.heure_fin,
            "nb_employes": b.nb_employes
        } for b in besoins])
    finally:
        session.close()

@app.route("/planning_global", methods=["GET"])
def get_planning_global():
    session = SessionLocal()
    try:
        horaires = session.query(Horaire).all()
        employes = session.query(Employe).all()

        # Structure : { employe_id: { "nom": ..., "prenom": ..., "jours": { "Lundi": "...", "Mardi": "..." } } }
        result = []
        jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

        for e in employes:
            planning_employe = {jour: "Repos" for jour in jours_semaine}
            for h in horaires:
                if h.id_employe == e.id:
                    planning_employe[h.jour] = f"{h.heure_debut} - {h.heure_fin}"
            result.append({
                "nom": e.nom,
                "prenom": e.prenom,
                "planning": planning_employe
            })

        return jsonify(result)

    finally:
        session.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
