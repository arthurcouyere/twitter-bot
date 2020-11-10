# twitter-bot

Tweete les mots du slip de la langue française du slip. Largement inspiré par le  [@botducul](https://twitter.com/botducul) (lexique identique, mais code en Python) et le [@botsupervnr](https://twitter.com/botsupervnr). 

Poste sur [@botduslip](https://twitter.com/botduslip).

Stocke la position du dernier mot tweeté dans une base Redis.

## Environnement de développement

### Pré-requis

Installer Redis pour le stockage de dernier mot tweeté.

### Configuration

Pour l'authentification Twitter, créer un fichier `.env` contenant les variables d'environnement suivantes :
```ini
REDIS_URL=redis://localhost:6379/0
CONSUMER_KEY=### A RECUPERER DEPUIS SON COMPTE TWITTER
CONSUMER_SECRET=### 
ACCESS_KEY=###
ACCESS_SECRET=###
```

Le script charge automatiquement le fichier s'il est présent sauf si les variables d'environnement sont déjà définies

## Déploiement en production

Pour déployer l'application sur Heroku depuis Ubuntu, se placer dans le répertoire ou a été cloné le dépot git en lancer les commandes suivantes :

```bash
sudo snap install --classic heroku
heroku login
heroku apps:create botduslip
heroku addons:create heroku-redis:hobby-dev -a botduslip
git push heroku main
heroku ps:scale clock=1
```

Pour voir les logs :
```bash
heroku logs --tail
```

Pour savoir quelle est la dernière position de mot dans la base Redis :
```bash
export REDIS_URL=$(heroku config | grep REDIS | awk '{print $2}')
redis-cli -u $REDIS_URL get twitter-bot.last_pos
```