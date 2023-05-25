import os
import requests
import json
from termcolor import colored


os.system("cls")


def send_webhook(url, file_name, email, phrase):
    if file_name is None:
        data = {
            "embeds": [
                {
                    "title": "Résultat de la recherche",
                    "description": "Rien n'a été trouvé !",
                    "color": 0xFF0000
                }
            ]
        }
    else:
        data = {
            "embeds": [
                {
                    "title": "Résultat de la recherche",
                    "description": f"Le mot `{email}` a été trouvé dans le fichier `{file_name}`.",
                    "fields": [
                        {
                            "name": "Phrase complète",
                            "value": phrase
                        }
                    ]
                }
            ]
        }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code != 204:
        print("Une erreur s'est produite lors de l'envoi du webhook Discord.")

def search_email_in_files(folder_path, email, webhook_url):
    files = os.listdir(folder_path)
    for file_name in files:
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r") as file:
                content = file.read()
                if email in content:
                    lines = content.split("\n")
                    for line in lines:
                        if email in line:
                            phrase = line.strip()
                            send_webhook(webhook_url, file_name, email, phrase)
                            return
    send_webhook(webhook_url, None, None, None)

# Demande de l'email à rechercher
email_to_search = input("""


                                   [+] Bonjour, que voulez-vous chercher ? : """)

# Chemin du dossier contenant les fichiers .txt
database_folder = "Database"

# Saisie de l'URL du webhook Discord
print(" ")
webhook_url = input("               [+] Veuillez entrer l'URL du webhook Discord afin de recevoir le résultat : ")

# Recherche de l'email dans le dossier et envoi du résultat au webhook Discord
search_email_in_files(database_folder, email_to_search, webhook_url)