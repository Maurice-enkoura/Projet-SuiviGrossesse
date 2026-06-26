🤰 SuiviGrossesse

Plateforme web de suivi médical de grossesse permettant aux patientes de suivre l'évolution de leur grossesse, de gérer leurs rendez-vous médicaux et de communiquer avec les professionnels de santé.

 Fonctionnalités
 Authentification sécurisée avec JWT
 Gestion des patientes, médecins et administrateurs
 Prise et gestion des rendez-vous
 Suivi des consultations prénatales
 Gestion des traitements et prescriptions
 Documentation de l'API avec Swagger
 Interface responsive et moderne
 Stack technique
Technologie	Utilisation
Backend	Django + Django REST Framework
Frontend	Vue.js 3 + Vite + Tailwind CSS
Base de données	MySQL
Authentification	JWT (JSON Web Token)
Documentation API	Swagger / OpenAPI
Gestion de version	Git & GitHub
 Installation
 Cloner le projet
git clone https://github.com/Maurice-enkoura/Projet-SuiviGrossesse.git
cd Projet-SuiviGrossesse
 Installation du Backend
cd backend-django

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

Le serveur démarre sur :

http://127.0.0.1:8000/
 Installation du Frontend
cd frontend-vue

npm install

npm run dev

Le frontend démarre sur :

http://localhost:5173/
 Documentation de l'API

Swagger :

http://127.0.0.1:8000/api/docs/

Schéma OpenAPI :

http://127.0.0.1:8000/api/schema/
 Structure du projet
Projet-SuiviGrossesse/
│
├── backend-django/
│   ├── api/
│   ├── config/
│   ├── requirements.txt
│   └── manage.py
│
├── frontend-vue/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── README.md
└── .gitignore
 Comptes de démonstration
Rôle	Email	Mot de passe
Patiente	patient@test.com	password123
Médecin	dr.martin@test.com	doctor123
Administrateur	admin@test.com	admin123

 Auteur

Maurice Enkoura

GitHub : @Maurice-enkoura