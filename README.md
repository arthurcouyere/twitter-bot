# twitter-bot

Largement inspiré par le  [@botducul](https://twitter.com/botducul) (lexique identique, mais code en Python). Tweete tous les jours un mot de la langue française du slip.

Poste sur [@botduslip](https://twitter.com/botduslip).

### Configuration
Pour l'authentification Twitter, créer un fichier `.env` contenant les variables d'environnement suivantes :
```
CONSUMER_KEY=###
CONSUMER_SECRET=###
ACCESS_KEY=###
ACCESS_SECRET=###
```

Pour charger le fichier :
* Utiliser le script `load_env.sh` depuis un shell
* Dans VSCode, ajouter les lignes suivantes au fichier `.vscode/launch.json` :

```
    "configurations": [
        {
            "envFile": "${workspaceFolder}/.env"
        }
    ]
```