import requests

url = "http://127.0.0.1:5000/login"

# 👇 Mets ici un email et mot de passe d'un employé de ta base
payload = {
    "email": "emma.durand@mail.com",
    "mot_de_passe": "123"
}

response = requests.post(url, json=payload)

print("Code de réponse:", response.status_code)
print("Contenu de la réponse:", response.json())
