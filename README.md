# P10 : API Django Rest Framework pour la gestion de projet 

Projet réalisé dans le cadre du développement d'une API pour la société SoftDesk.

Il s'agit d'une application permettant de remonter et de suivre des problèmes techniques liés à des projets. Ce produit est destiné à des entreprises en B2B.

---

## Fonctionnalités

- Authentification JWT (inscription, connexion, access/refresh token)
- Gestion des utilisateurs (âge minimum 15 ans)
- Gestion de projets (back-end, front-end, iOS, Android)
- Gestion des contributeurs par projet
- Suivi des problèmes (issues) avec priorité, balise et statut
- Commentaires sur les issues (identifiés par UUID)
- Pagination (5 éléments par page)
- Permissions par rôle

---

## Architecture

L'API suit un style architectural RESTful et est divisé en 2 applications :
- Application de gestion des comptes utilisateurs : `accounts`
- Application métier de gestion des projets : `projects`


---

## Structure du projet

```
P10_SoftDesk_Support/

    README.md                               # Documentation
    .gitignore                              # Liste des dossiers et fichiers à ignorer pour le repository
    Pipfile & Pipfile.lock                  # Fichiers Pipenv pour gestion des dépendances et de l'environnement virtuel
    .env                                    # Clé secrète (non inclus dans le repository)
    .env.example                            # Template à copier en .env et à compléter avec la clé secrète
    
    SoftDesk/                               # Répertoire principal projet Django
        accounts/                           # Application de gestion des comptes utilisateurs 
        SoftDesk/                           # Configuration globale du projet (settings, urls)
        projects/                           # Application métier - projects, issues, comments
        db.sqlite3                          # Base de données (non-inclue dans le repository)
        manage.py                           # Fichier de gestion de commandes Django
        

```

---

## Technologies utilisées

- Python / Django
- Django REST Framework
- Simple JWT
- drf-nested-routers
- python-decouple
- flake-8

---

## Installation 

### Prérequis :

- Python 3.10 ou plus récent
- Connexion internet

### Cloner le repository : 

```bash
git clone https://github.com/duncan-g-hub/P10_SoftDesk_Support.git
cd P10_SoftDesk_Support
```

---

### Installer des dépendances avec Pipenv

```bash
pip install pipenv
pipenv install
```


---

### Activer l'environnement virtuel : 

```bash
pipenv shell
```
---

### Configurer les variables d'environnement

Copier `.env.example` en `.env` et renseigner la SECRET_KEY

Pour générer une nouvelle clé secrète, exécuter la commande suivante :

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copier la valeur retournée et la renseigner dans le fichier `.env`.

---

### Appliquer les migrations

```bash
cd SoftDesk
python manage.py migrate
```

---

### Lancer le serveur de l'application

Lancement serveur local : 
```bash
python manage.py runserver
```

---

## Authentification

L'API utilise JWT. Les tokens ont les durées de vie suivantes :
  - Access token : 5 minutes 
  - Refresh token : 1 jour


### Obtenir un token

Inclure vos identifiants au sein du body d'une requête POST à l'adresse : http://127.0.0.1:8000/api/token/

```json
{
  "username": "votre_username",
  "password": "votre_mot_de_passe"
}
```

Exemple de réponse : 
```json
{ 
  "refresh": "refreshtoken", 
  "access": "accesstoken"
}
```
Conserver les deux tokens. 
Le token d'access devra être renseigné dans le header sous la clé Authorization, précédé de "Bearer" afin d'accéder aux endpoints protégés de l'API.

`Authorization : Bearer <access_token>`


### Rafraichir un token

Inclure le refresh token au sein du body d'une requête POST à l'adresse : http://127.0.0.1:8000/api/token/refresh/
```json
{ 
  "refresh": "refreshtoken"
}
```

Exemple de réponse :
```json
{ 
  "access": "accesstoken"
}
```

---

## Endpoints

### Utilisateurs

| Méthode | URL | Description | Auth |
|---|---|---|---|
| POST | `/api/users/` | Créer un compte | Non |
| GET | `/api/users/` | Lister les utilisateurs | Oui |
| GET | `/api/users/{id}/` | Détail d'un utilisateur | Oui |
| PUT/PATCH | `/api/users/{id}/` | Modifier son compte | Oui (propriétaire) |
| DELETE | `/api/users/{id}/` | Supprimer son compte | Oui (propriétaire) |

### Projets

| Méthode | URL | Description | Auth |
|---|---|---|---|
| GET | `/api/projects/` | Lister les projets | Oui |
| POST | `/api/projects/` | Créer un projet | Oui |
| GET | `/api/projects/{id}/` | Détail d'un projet | Oui |
| PUT/PATCH | `/api/projects/{id}/` | Modifier un projet | Oui (auteur) |
| DELETE | `/api/projects/{id}/` | Supprimer un projet | Oui (auteur) |

### Contributeurs

| Méthode | URL | Description | Auth |
|---|---|---|---|
| GET | `/api/projects/{project_id}/contributors/` | Lister les contributeurs | Oui |
| POST | `/api/projects/{project_id}/contributors/` | Ajouter un contributeur | Oui (auteur du projet) |
| DELETE | `/api/projects/{project_id}/contributors/{id}/` | Retirer un contributeur | Oui (auteur du projet) |

### Issues

| Méthode | URL | Description | Auth |
|---|---|---|---|
| GET | `/api/projects/{project_id}/issues/` | Lister les issues | Oui |
| POST | `/api/projects/{project_id}/issues/` | Créer une issue | Oui (contributeur) |
| GET | `/api/projects/{project_id}/issues/{id}/` | Détail d'une issue | Oui |
| PUT/PATCH | `/api/projects/{project_id}/issues/{id}/` | Modifier une issue | Oui (auteur) |
| DELETE | `/api/projects/{project_id}/issues/{id}/` | Supprimer une issue | Oui (auteur) |

### Commentaires

| Méthode | URL | Description | Auth |
|---|---|---|---|
| GET | `/api/projects/{project_id}/issues/{issue_id}/comments/` | Lister les commentaires | Oui |
| POST | `/api/projects/{project_id}/issues/{issue_id}/comments/` | Créer un commentaire | Oui (contributeur) |
| GET | `/api/projects/{project_id}/issues/{issue_id}/comments/{id}/` | Détail d'un commentaire | Oui |
| PUT/PATCH | `/api/projects/{project_id}/issues/{issue_id}/comments/{id}/` | Modifier un commentaire | Oui (auteur) |
| DELETE | `/api/projects/{project_id}/issues/{issue_id}/comments/{id}/` | Supprimer un commentaire | Oui (auteur) |

---

## Modèles de données

### User
| Champ | Type | Description |
|---|---|---|
| username | string | Nom d'utilisateur |
| password | string | Mot de passe (haché) |
| birth_date | date | Date de naissance (format JJ/MM/AAAA, min. 15 ans) |
| can_be_contacted | boolean | Consentement contact |
| can_data_be_shared | boolean | Consentement partage de données |

### Project
| Champ | Type | Description |
|---|---|---|
| name | string | Nom du projet |
| description | text | Description |
| type | string | `back-end`, `front-end`, `iOS`, `Android` |

### Issue
| Champ | Type | Description |
|---|---|---|
| name | string | Titre de l'issue |
| description | text | Description |
| priority | string | `LOW`, `MEDIUM`, `HIGH` |
| tag | string | `BUG`, `FEATURE`, `TASK` |
| status | string | `To Do`, `In Progress`, `Finished` |
| assigned_to | Contributor | Contributeur assigné (optionnel) |

### Comment
| Champ | Type | Description |
|---|---|---|
| description | text | Contenu du commentaire |
| uuid | UUID | Identifiant unique (auto-généré) |

---

## Permissions

| Rôle | Droits |
|---|---|
| Non authentifié | Créer un compte uniquement |
| Authentifié | Lire tous les projets, créer un projet |
| Auteur du projet | Modifier/supprimer le projet, gérer les contributeurs |
| Contributeur | Créer/modifier/supprimer ses propres issues et commentaires |


---

## Contact

Pour toute question :  
Duncan GAURAT - duncan.dev@outlook.fr

            
