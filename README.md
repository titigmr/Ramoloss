# Ramoloss

![CI_badge](https://github.com/titigmr/ramoloss/actions/workflows/main.yml/badge.svg)

## Installation sur un serveur Discord

...



## Modules disponibles

* [Dice](#dice) : simule des lancés de dés
* [UFD](#Ultimate-Frame-Data-(UFD)) : retourne les statistiques des personnages du jeu SSBU
* [Poll](#poll) : permet de créer des sondages
* [Johns](#johns) : prédit si un joueur est de mauvaise foi

<br>

### Dice
Module qui permet de simuler des lancers de dés. Quelques exemples d'utilisations :

Lance un dé à six faces
```
$d 1d6
```

Lance deux dés à six faces
```
$d 2d4
```

Choisis un nombre aléatoire entre -101 et 150
```
$d 1d[-101:150]
```

Additionne un lancé de dé à six face puis un dé à huits faces en affichant les valeurs intémédiaires
```
$d 1d6 + 1d8 -v
```

Soustrait un lancé de dé à six face puis un dé à huits faces sans afficher les valeurs intermédiaires
```
$d 1d6 - 1d8
```

Ajoute 6 à un lancé de dé à six faces
```
$d 1d6 + 6
```

### Johns

...

### Ultimate Frame Data (UFD)

Utilise comme une API le site des statistiques des personnages du jeu Super Smash Bros Ultimate [(UFD)](https://www.ultimateframedata.com).

Un exemple de commande :

```
$ufd wario [fair]
```

<br>

<img src='img/example_ufd.gif'>

<br>
<br>

### Poll
Module permettant de créer des sondages sur Discord. Voici un exemple d'utilisation :

```
Create a simple poll.
$poll Qui joue ?

For advanced polls use the folowing syntax:
$poll {title} [Option1] [Option2] [Option 3] ...

Note: options are limited at 21.
```

## Déploiement
Le bot peut se déployer avec Docker-compose ou python directement.

Dans un premier temps, mettre le token discord en tant que variable d'environnement.
```bash
export DISCORD_TOKEN=<token>
```

Cloner le répertoire en local, puis aller dans le dossier.

```bash
git clone https://github.com/titigmr/Ramoloss.git
cd Ramoloss
```

Lancer le conteneur.

```bash
docker-compose up
```
