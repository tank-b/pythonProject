
#Créer des jetons JWT
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
#Utiliser des pages html
from flask import render_template
#Utiliser Flask et récupérer les variables d'un formulaire
from flask import Flask, request

#Elements de formulaire
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

#Connexion à la base de données
import mysql.connector

#Bcrypt
import bcrypt


app = Flask(__name__)

#@app.route('login/', methods=['POST'])
#app.config['JWT_SECRET_KEY'] = 'secret_key'
#jwt = JWTManager(app)

#Connection à la base de données
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bubu3000",
    database="djangoProject"
)


@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/traitement',methods = ['GET','POST'])
def traitement():
    #On récupère les variables rentrés par l'utiilsateur
    login = request.form['login']
    password = bytes(request.form['password'].encode('utf-8'))


    #La ligne suivante permet de tester l'output
    #print_salt = salt.decode('utf-8')

    # Si l'utilisateur a bien rentré un login, on va chercher le mot de passe
    if len(login) >= 1:
        sql_check = "SELECT * FROM djangoProject_students where login = '%s' " % login
        mycursor = mydb.cursor()
        mycursor.execute(sql_check)
        check = mycursor.fetchall()
        # S'il n'y a pas de mot de passe associé en BD, l'utilisateur n'existe pas
        if len(check) == 0:
            return "Accès refusé."

        #On récupère le salt dans le tableau où le login est égal à login
        sql_salt = "SELECT salt from djangoProject_students where login = '%s' " % login
        mycursor = mydb.cursor()
        mycursor.execute(sql_salt)
        salt = mycursor.fetchall()
        #On le transforme en type bytes pour qu'il puisse être utilisé par la suite
        salt = bytes(salt[0][0].encode("utf-8"))

        # Génération du mdp haché à partir de celui rentré par l'utilisateur + du salt qu'on a trouvé dans sa table
        typed_password = bcrypt.hashpw(password, salt)

        #On récupère le mot de passe hashé dans la DB
        sql_password = "SELECT hashed from djangoProject_students where login = '%s' " % login
        mycursor = mydb.cursor()
        mycursor.execute(sql_password)
        real_password = mycursor.fetchall()
        real_password = bytes(real_password[0][0].encode("utf-8"))


        # Si le mot de passe obtenu correspond au mot de passe tapé puis haché, alors on affiche le formulaire 2
        if real_password == typed_password:
            return render_template('resultats.html', login=login)
        # Si le mot de passe obtenu ne correspond pas, on refuse l'accès
        else:
            return "Accès refusé."


    else:
        return "Merci de taper un login !"







if __name__ == "__main__":
    app.run(debug=True)