# Sécurité des réseaux sans fil

## Laboratoire 802.11 MAC

> Auteurs    : Frueh Loic - Muaremi Dejvid    
> Enseignant : Abraham Rubinstein   
> Assistants : Yohan Martini   
> Date       : 20.03.2019   

---
## Utilisation des outils
Pour passer une interface en mode monitor, il faudra utiliser la commande suivante (vérifiez avec ```ifconfig```que votre interface s'appelle bien ```wlan0```. Sinon, utilisez le nom correct dans la commande):

```bash
sudo airmon-ng start wlan0
```
Vous retrouverez ensuite une nouvelle interface ```wlan0mon``` qui fonctionne en mode monitor.

Pour lancer uun scan avec airodump-ng :
```bash
sudo airodump-ng wlp4s0mon
```

Pour desactiver le mode monitor :
```bash
sudo airmon-ng stop wlp4s0mon
sudo service network-manager stop
sudo rm /var/lib/NetworkManager/NetworkManager.state
sudo service network-manager start
```
Vous retrouverez ensuite votre ancienne interface ```wlan0```.


## Réponses aux questions

### 1. Détecter si un ou plusieurs clients 802.11 spécifiques sont à portée

__Question : quel type de trames sont nécessaires pour détecter les clients de manière passive ?__
Pour la détection et le suivi de client 802.11, nous utilisons les "probes requests" qui sont utilisée par celui-ci de manière automatique afin de trouver les access points disponible.

__Question : pourquoi le suivi n'est-il plus possible sur iPhone depuis iOS 8 ?__
Il n'est pas impossible de suivre un iPhone sous iOS > 8, c'est juste plus compliqué. Depuis iOS 8, Apple a mis en place une génération aléatoire des adresses MAC lors de l'envoie de "probes requests" pour ses téléphones. Cependant, une fois que le téléphone a est connecté à un access point ou n'est plus en mode veille, a l'écran allumé, cette sécurité est enlevée et c'est la veritable adresse MAC qui est envoyée.


### 2. Clients WiFi bavards

Nous avons voulu utiliser des threads dans notre script afin de traiter le scan et l'affichage des résultats en parallèle. Ceci fonctionne, cependant, lorsque l'on quitte le script à l'aide d'un ctrl-c celui-ci affiche des erreurs. Nous avons eu beau chercher diverses solutions aucune n'a résolu le problème.