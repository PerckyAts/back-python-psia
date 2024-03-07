# 1. Dépendances

**INSTALLER PYTHON**

```
    sudo apt install python3
```


**INSTALLER PYTHON-VENV**

>Permet de créer un environnement virtuel pour Python

```
    sudo apt install python3-venv
```

# 2. Création d'environnement de dev local

- Répertoire du travail dossier code

```
    cd code/
```

- Création dossier env
  
```
    python3 -m venv env
```

- Activation de l'environnement env

```
    source env/bin/activate
```

- Installation des dépendances Python
  
```
    pip install -r requirements.txt
```


# 3. Lancement du serveur

> NB: Nom du serveur > Uvicorn

**Exécution du serveur :**

```
    python3 main.py
```


# 3. Migration des tables

> Utililiser si on aapplique des modification au niveau des tables
>
> ex: Ajout  des relations, insertion des nouveaux  colonnes, etc...


## NB: Exécuter les commandes suivantes seulement s'il n'y avait pas un dossier alembic dans le code:

1. Initialiser alembic

```
    alembic init alembic
```

2. Éditer la ligne suivante dans le fichier **_alembic.ini_** dans le dossier code
   
>Remplacer:
>
>>DB_USER = Nom d'utilisateur de la base de donées
>
>>DB_PASSWORD =  Passeword de la base de données
>
>>DB_HOST = Host de la base de données
>
>>DB_PORT = port de la base de données
>
>>DB_NAME = Nom de la base de donnée (jarvis)
>

```
    sqlalchemy.url = postgresql+psycopg2://DB_USER:DB_PASSWORD@DB_HOST:DB_PORT/DB_NAME
``` 


## NB: Exécuter les commandes suivantes si le dossier alembic est créé ou déjà dedans:

1. Appliquer la migration

```
    alembic revision -m "Add new table"
```
   
```
    alembic upgrade head
```

### Notes:

1. ORM

>   ORM UTILISER "SQLALCHEMY"

2. Pour installer une package :

```
    pip install PACKAGE_NAME
```

3. Après avoir installé une package, exécutez la commande suivante :


```
    pip freeze > requirements.txt
```


