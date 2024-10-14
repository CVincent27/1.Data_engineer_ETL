import requests
import base64
import json
import os

# Remplacez ces valeurs par vos propres informations
CLIENT_ID = '5e3fcd8ba2f046d9862f645e4a620eda'
CLIENT_SECRET = '003729ad92684faa994340f14b190f7c'
REDIRECT_URI = 'http://127.0.0.1:5500/'
SCOPE = 'user-read-private user-read-email'

# Étape 1 : Obtenir le code d'autorisation
def get_authorization_code():
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    print(f"Code d'authentification : {auth_url}")
    
    # Entrer le code d'autorisation
    auth_code = input("Entrez le code : ")
    return auth_code

# Étape 2 : échanger le code contre le token
def get_access_token(auth_code):
    token_url = "https://accounts.spotify.com/api/token"
    
    # Créez un en-tête d'autorisation
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # Les données pour l'échange
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }
    
    response = requests.post(token_url, headers=headers, data=data)
    token_info = response.json()
    
    if 'access_token' in token_info:
        return token_info['access_token']
    else:
        print("Erreur lors de l'obtention du jeton d'accès")
        print(token_info)
        return None

# Étape 3 : jeton d'accès pour accéder à la data utilisateur
def get_user_data(access_token):
    user_url = "https://api.spotify.com/v1/me"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get(user_url, headers=headers)
    user_data = response.json()
    
    return user_data

if __name__ == '__main__':
    auth_code = get_authorization_code()  # Étape 1
    access_token = get_access_token(auth_code)  # Étape 2
    
    if access_token:
        user_data = get_user_data(access_token)  # Étape 3
        print(json.dumps(user_data, indent=4))  # Affiche les données utilisateur
