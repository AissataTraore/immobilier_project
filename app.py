
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import pymysql
app = Flask(__name__)


# Configuration de la base de données MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Utilisateur MySQL
app.config['MYSQL_PASSWORD'] = ''  # Mot de passe MySQL
app.config['MYSQL_DB'] = 'customer_base'  # Base de données MySQL
# mysql = MySQL(app)

# Initialisation de l'extension MySQL
#mysql = MySQL(app)

methods=['POST', 'PUT', 'GET', 'PATCH', 'DELETE']

def get_db():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/', methods=['GET'])
def list_customers():
    per_page = int(request.args.get('per_page', 10))
    page = int(request.args.get('page', 1))
    offset = (page - 1) * per_page
    
    # Récupération d'une connexion à la base de données && Création d'un curseur pour exécuter des requêtes SQL
    cur = get_db().cursor()
    cur.execute(f"SELECT * FROM client LIMIT {offset}, {per_page}")
    customers = cur.fetchall()

    # Compter le nombre total de lignes
    cur.execute("SELECT COUNT(*) FROM client")
    total_customers = 1000 #cur.fetchone()[0]
    
    total_pages = (total_customers // per_page) + (total_customers % per_page > 0)
    
    return render_template('index.html', customers=customers, page=page, per_page=per_page, total_pages=total_pages)

@app.route('/create', methods=['GET'])
def add_form ():
    return render_template('create.html')

@app.route('/add', methods=['POST'])
def add_client_form ():
    if request.method == 'POST':  # Check if the request method is POST
        nom = request.form['nom']  # Access form field value using dictionary access
        prenom = request.form['prenom']
        cur = get_db().cursor()
        cur.execute("INSERT INTO client(nom, prenom) VALUES (%s, %s)", (nom, prenom))
        cur.connection.commit()
        return redirect(url_for('list_customers'))

@app.route('/edit/<int:id>', methods=['GET, POST'])
def edit_form(id):
    if request.method == 'GET':
        cur = get_db().cursor()
        cur.execute("SELECT * FROM client WHERE id = %s", (id,))
        customer = cur.fetchone()
        return render_template('edit.html', customer=customer)
    elif request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        cur = get_db().cursor()
        cur.execute("UPDATE client SET nom=%s, prenom=%s WHERE id=%s", (nom, prenom, id))
        cur.connection.commit()
        return redirect(url_for('list_customers')) 

if __name__ == '__main__':
    app.run(debug=True)