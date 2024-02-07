

#Cette page nous servira à importer les étudiants dans la BD avec un mot de passe haché.
import mysql.connector

import bcrypt
class Students:

    def __init__(self, login, prenom, nom, email, password):
        self.login = login
        self.prenom = prenom
        self.nom = nom
        self.email = email
        self.password = password
        self.students_list = []

    def add_student(self, student):
        self.students_list.append(student)

    def get_students(self):
        return self.students_list

# Créer un tableau avec 4 personnes dedans

student1 = Students("sjohnson", "Skye", "Johnson", "skyejohnson@mail.com","hibou1234")
student2 = Students("schi", "Shang", "Chi", "shangchi@mail.com","genou1234")
student3 = Students("omunroe", "Ororo", "Munroe", "ororomunroe@mail.com","caillou1234")
student4 = Students("kwagner", "Kurt", "Wagner", "kwagner@mail.com", "bijou1234")

#Créer une liste des objets "student"
student1.add_student(student1)
student1.add_student(student2)
student1.add_student(student3)
student1.add_student(student4)

#Accéder aux objets dans la liste des étudiants
students_list = student1.get_students()




#Créer une fonction de hachage de mot de passe (qui permettra de faire en sorte que le sel soit toujours différent)

##Fonction pour définir le salt
def make_salt():
    salt = bcrypt.gensalt()
    return salt



##Fonction pour hacher un mot de passe
def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

#Connexion à la base de donnée :
mydb = mysql.connector.connect(

    host="localhost",
    user="root",
    password="bubu3000",
    database="djangoProject"

)

mycursor = mydb.cursor()
#Créer une boucle qui remplace le mot de passe en clair dans le tableau par le mot de passe haché.

i=0

while i < 4:
    password = students_list[i].password
    ##Appel de la fonction de salt
    salt = make_salt()
    ##Appel de la fonction hashage du mot de passe
    hashed = hash_password(password)
    ##Remplacer la valeur du mdp clair par un mdp haché
    students_list[i].password = hashed
    ##Rentrer la valeur dans la base de données
    mycursor.execute("INSERT INTO djangoProject_students (login, first_name, last_name, email, hashed, salt) VALUES (%s, %s, %s, %s, %s, %s)", (students_list[i].login, students_list[i].prenom, students_list[i].nom, students_list[i].email, hashed, salt))
    mydb.commit()
    #Incrémenter i
    i += 1
mycursor.close()
mydb.close()