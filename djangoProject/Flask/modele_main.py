#Pour bien comprendre :
#Gérer le cas d'inscrire un utilisateur
#stocker le JWT en, DB pour éviter que 2 sessions concurrentes

#Dépendances
from flask import Flask, render_template, request, redirect, url_for, make_response
#generation auto des éléments de formulaires
from flask_wtf import FlaskForm
#Lib de vérification de données
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
#gestion des dates
import datetime
#JWT et Hash de mot de passe
import jwt
import bcrypt
import mysql.connector
#utilisation a coté un fichier env.py non gitté pour mettre tout ce qui est conf
## Conseil : migrer toutes les données de conf dans le fichier et gérer un contexte dev et prod


#initialise mon app Flask
app = Flask(__name__)
#app.secret_key = env.conf["secretLocal"]
#jwt_secret_key = env.conf["secretJwt"]

#class pour le formulaire de connexion
class LoginForm(FlaskForm):
    #Role : Avoir un objet pour gérer les données de mon formulaire
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Connexion')

def verify_password(plain_password, hashed_password, stored_salt):
    #Prend en paramère le mdp en clair, le hash, le salt associé au hash
    salt = stored_salt.encode('utf-8')
    hashed_attempt = bcrypt.hashpw(plain_password.encode('utf'),salt)
    #Version a tester checkpw(password, hashed_password) en bytestring
    hashed_password = hashed_password.encode('utf-8')
    #renvoi un bool ok pas ok
    return hashed_attempt == hashed_password

def generate_jwt(username):
    #Generation de token
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, jwt_secret_key, algorithm='HS256')
    return token



#@app.route('/register', methods=['GET','POST'])
# Page permettant de se créer un compte


#Route de connexion
@app.route('/login', methods=['GET','POST'])
def login():
    #Je défini mon formulaire
    form = LoginForm()
    # token = request.cookies.get('jwt')
    # payload = jwt.decode(token, jwt_secret_key, algorithms=['HS256'])
    # username = payload['username']
    # if username == "Tim":
    #     return "Tu es deja connecté"

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        #J'ai mes identifiants je vais aller cherche en DB ce qu'il me faut
        #pour comparer
        # Conf BDD
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=bubu3000,
            database="djangoProject"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT password, salt FROM users WHERE login = %s", (username,))
        user_data = cursor.fetchone()

        if user_data:
            stored_hashed_password = user_data['password']
            stored_salt = user_data['salt']
            #J'appelle la fonction de verif
            if verify_password(password, stored_hashed_password, stored_salt):
                #Si mot de passe vérifié, alors je génère mon JWT
                jwt_token = generate_jwt(username)
                #Je prepare ma réponse avec une redirection
                response = make_response(redirect(url_for('protected')))
                #Dans ma réponse je mettrais a jour les cookis
                response.set_cookie('jwt',jwt_token)
                response.set_cookie('livecampus', "coucou")
                return response
                #Je renvoi ma réponse
            else:
                #Un user a été trouvé mais le mot de passe est pas bon
                return "Erreur"
        else:
            #L'utilisateur a pas été trouvé
            return "Erreur"

        conn.close()
    #Si la page n'a pas été appelée eb post et ou si le formulaire n'est pas valide
    return render_template('login.html', form=form)

@app.route('/protected')
def protected():
    try:
        #Je récupère le token
        token = request.cookies.get('jwt')
        payload = jwt.decode(token, jwt_secret_key, algorithms=['HS256'])
        username = payload['username']
        return f'Bienvenue à toi {username}'
    except jwt.ExpiredSignatureError:
        response = make_response(redirect(url_for('login')))
        return response
    except jwt.InvalidTokenError:
        response = make_response(redirect(url_for('login')))
        return response

if __name__ == "__main__":
    app.run(debug=True)