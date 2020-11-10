# twitter-bot

Tweete les mots du slip de la langue française du slip. Largement inspiré par le  [@botducul](https://twitter.com/botducul) (lexique identique, mais code en Python) et le [@botsupervnr](https://twitter.com/botsupervnr). 

Poste sur [@botduslip](https://twitter.com/botduslip).

### Configuration
Pour l'authentification Twitter, créer un fichier `.env` contenant les variables d'environnement suivantes :
```
CONSUMER_KEY=###
CONSUMER_SECRET=###
ACCESS_KEY=###
ACCESS_SECRET=###
```

Le script charge automatiquement le fichier s'il est présent sauf si les variables d'environnement sont déjà définies