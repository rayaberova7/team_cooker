# Projet Team Cooker
L'équipe de foot du mercredi de la DG LOL

## Getting started

```{bash}
git clone 
```

File > Open Folder > /home/onyxia/work/team_cooker/

```{bash}
pip install -r requirements.txt
```

## Lancer le projet

Remplir le .env avec ce template et les données dans le README du service PostgreSQL ouvert sur Onyxia :

```default
POSTGRES_HOST=xx
POSTGRES_PORT=5432
POSTGRES_DATABASE=xxx
POSTGRES_USER=xxx
POSTGRES_PASSWORD= xxx
POSTGRES_SCHEMA=foot
```

Pour initialiser la BDD :
```{python}
python -m src.utils.reset_database
```

Lancer l'API :

```{bash}
python src/app.py
```
Et aller sur le lien fourni lors de l'ouverture du service VSCode

