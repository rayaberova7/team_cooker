# Projet Team Cooker
L'équipe de foot du mercredi de la DG LOL

## Getting started

Ouvrir un VSCode sur Onyxia avec le port 9876 d'ouvert
```{bash}
git clone https://github.com/rayaberova7/team_cooker
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
uvicorn src.app:app --host 0.0.0.0 --port 9876
```
Et aller sur le lien fourni lors de l'ouverture du service VSCode

## Déployer l'API

Ouvrir un VSCode avec role admin pour kubernetes puis cloner le dépôt Git.
Push le code et dans github Actions, lancer le Image Build.
Une fois que l'image Docker est faite, aller sur VSCode et lancer :
```{bash}
# Supprimer l'ancien déploiement s'il a été fait
kubectl delete deployments.apps team-cooker-model-deployment 

# Déployer l'API
kubectl apply -f cd/deployment-api/

# Voir la création des pods
kubectl get pods
# Ils doivent avoir un status Running, si ce n'est pas le cas il faut investiguer

# Vérifier les logs d'un pod précis
kubectl describe pods team-cooker-model-deployment-XXXXXXXXX
```