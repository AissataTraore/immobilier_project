from flask import Flask

app = Flask(__name__)  # Utilisez _name_ pour initialiser l'application Flask

@app.route('/')
def index():
    return "Hello world!"  # Supprimez l'espace avant le point d'exclamation

if __name__ == "__main__":  # Vérifiez si le script est exécuté directement
    app.run()  # Lancez le serveur 