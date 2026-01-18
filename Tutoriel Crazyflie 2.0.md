# Présentation du Crazyflie 2.0

Tout d'abord, se référer à la page suivante : [Getting started with the Crazyflie 2.0 or Crazyflie 2.1(+)](https://www.bitcraze.io/documentation/tutorials/getting-started-with-crazyflie-2-x/)

## Informations générales

Le crazyflie 2.0 possède 4 LEDs : M1, M2, M3 et M4 (indiqué sur le drone).

Le sens avant du Crazyflie 2.0 est indiqué par un symbole situé entre les LEDs M4 et M1.

Le bouton marche/arrêt est situé devant à droite.

## Monter le Crazyflie 2.0

Les crazyflie seront normalement déjà montés, mais vous pouvez vous référer à cette section et les étapes suivantes si besoin.

Si les supports moteur en plastique sont abîmés :

1. Débranchez les fils moteur.
2. Retirer la partie en plastique endomagée.
3. Sortez le moteur (par le haut).
4. Remplacez la partie endomagée et remettez-la en place avec le moteur. Rebranchez ensuite le moteur.

Si une hélice est abîmée, faîtes attention au type d'hélice que vous allez remettre ensuite. Il en existe deux :

- hélice sens horaire (Clock-Wise, CW) : notée A, A1 ou A2 sur l'hélice
- hélice sens anti-horaire (Counter Clock-Wise, CCW) : notée B, B1 ou B2 sur l'hélice

Pour savoir où les placer, un symbole flèche vous indiquant le sens de rotation est présent sur chaque branche moteur du Crazyflie 2.0.

## Comportement du Crazyflie 2.0

### Initialisation et self-test

Pour démarrer le Crazyflie 2.0, celui-ci doit être connecté à une source de puissance (à la batterie ou par micro-usb).

Lors de l'allumage, le drone fait tourner chacune de ses hélices une par une (initialisation) puis effectue un self-test, dont les résultats seront indiqués par les LEDs M1 et M4.

- Test validé : La LED M4 clignote vert 5 fois rapidement
- Test non validé : La LED M1 clignote 5 fois rapidement en rouge, puis pause et recommence

PS : tant que le drone n'est pas sur une surface plane, l'initialisation n'aura pas lieu. Si vous le posez au sol et que les hélices ne tournent pas, attendez qu'il s'intialise, cela peut parfois prendre quelque secondes ou plus rarement quelques minutes.

### Signification des LEDs

- Drone allumé, rien à signaler : les LEDs bleues M2 et M3 sont allumées, et la LED M1 clignote rouge 2 fois toutes les secondes.
- Drone allumé mais pas encore calibré : les LEDs bleues M2 et M3 sont allumées, et la LED M1 clignote rouge toutes les 2 secondes.
- Drone connecté à la radio : la LED M4 clignote de manière irrégulière en vert et/ou en rouge.
- Batterie faible : la LED M1 est allumée en rouge.
- Drone en charge : la LED bleue M3 clignote, tandis que la LED bleue M2 est allumée.
- Drone en mode bootloader : les LEDs bleues M2 et M3 clignotent à peu près toutes les secondes.

## Problèmes hardware rencontrés

- Hélice abîmée -> remplacer l'hélice
- Hélice ne tournant pas bien (l'hélice est censée bien tourner lorsqu'on la fait tourner simplement avec les doigts) -> partie centrale de l'axe moteur trop enfoncée
- Sectionnement des câbles batterie par fatigue (les câbles doivent bien souvent être tordus pour permettre de ranger la batterie dans son deck) -> nécessité de resouder le(s) câble(s)
- Bouton marche/arrêt endommagé (impossibilité d'utilisation)
- Moteur endommagé (entraînement de l'hélice nul ou faible) -> remplacer le moteur

# Installation client

**Ubuntu/Linux**  

En premier lieu, dans le cmd, taper les lignes suivantes :  

```
sudo apt install git python3-pip libxcb-xinerama0 libxcb-cursor0
pip3 install --upgrade pip
```

Ensuite, configurer les autorisations *udev* :  

Tout d'abord,

```
sudo groupadd plugdev
sudo usermod -a -G plugdev $USER
```

Quitter la session puis revenir.
Copier-coller le bloc suivant :

```
cat <<EOF | sudo tee /etc/udev/rules.d/99-bitcraze.rules > /dev/null
# Crazyradio (normal operation)
SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="7777", MODE="0664", GROUP="plugdev"
# Bootloader
SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="0101", MODE="0664", GROUP="plugdev"
# Crazyflie (over USB)
SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5740", MODE="0664", GROUP="plugdev"
EOF
```

Cela fera apparaître le fichier 99-bitcraze.rules dans le dossier /etc/udev/rules.d  
Taper ensuite ces 2 lignes :  

```
sudo udevadm control --reload-rules
sudo udevadm trigger
```

On va ensuite installer librairies et client, mais avant cela, il est conseillé de créer un virtual environment (venv) afin de les y installer.
Pour ce faire :

```
python3 -m venv ~/.virtualenvs
```

A savoir que la librairie et le client ne sont supportés que sur Python3, donc toujours utiliser python3 et pip3.
Pour activer le venv :

```
source ~/.virtualenvs/bin/activate
```

Dans celui-ci, installer crazyflie library (cflib) :

```
pip3 install cflib
```

Puis installer le client :

```
pip3 install cfclient
```

Pour accéder au client, il suffit de taper la ligne suivante lorsque l'on se trouve dans le venv :

```
cfclient
```

## Guide utilisation cfclient

Vous pouvez trouver le guide du cfclient dans la page suivante : [Userguide cfclient GUI](https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/userguides/userguide_client/)

## Identifier les URI (Uniform Resource Identifier)

Il existe plusieurs URI en fonction de la connection que l'on utilise entre le cfclient et le Crazyflie 2.0.

Nous avons notamment : *radio, serial, usb, debug et udp*.

Dans la partie *Select interface* du cfclient, on peut trouver les drones disponibles en effectuant un scan. Par exemple, on pourra trouver :

- *radio://0/10/2M* : interface radio, clé USB 0, channel radio 10 and vitesse radio 2 Mbit/s
- *usb://0* : drone connecté en micro-usb

(Les autres types d'URI sont détaillés [ici](https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/python_api/), mais nous allons normalement ne rencontrer que les URI de type *radio* et *usb*)

# Mettre à jour les firmwares

Il est nécessaire de mettre à jour les firmwares (du Crazyflie 2.0 et de la Crazyradio PA) afin de s'assurer de ne rencontrer aucun problème à ce niveau-là.

Pour mettre à jour le firmware du drone, il faut le brancher en micro-usb et ouvrir le cfclient, et allumer le drone. Comme le drone est connecté via micro-usb, sélectionnez *usb://0* dans la liste, et connectez-vous. N'oubliez pas de brancher le Crazyradio PA sur votre ordinateur.

Rendez vous ensuite dans le menu *Connect* puis *Bootloader*. Si dans l'onglet *Connect Crazyflie* le drone n'est pas sélectionné, sélectionnez-le. Il se peut que la version *radio* de votre drone soit disponible, dans ce cas essayez de vous connecter avec cette adresse-là. Normalement la version la plus récente du firmware est déjà sélectionnée dans l'onglet *From release* (préférez plutôt cette méthode d'installation) et la plateforme devrait déjà être bien sélectionnée également. Aussi, vous devriez donc pouvoir cliquer sur le bouton *Program*. Si ce n'est pas le cas, vous avez plusieurs options possibles :

- Essayez la version *usb* et la version *radio* de l'adresse.
- Essayez d'éteindre et de rallumer le drone.
- Essayez de vous mettre en mode bootloader (expliqué dans la prochaine section) et de refaire les étapes décrites plus haut.

## Mode bootloader

Pour vous mettre en mode bootloader, éteignez le drone, puis pour le rallumer, appuyez sur le bouton marche/arrêt jusqu'à que les LEDs bleues M2 et M3 clignotent. Vous êtes maintenant en mode bootloader. Pour sortir du mode bootloader, rappuyez simplement sur le bouton marche/arrêt.

## Cold reboot

Si vous avez un quelconque problème avec le firmware du drone, par exemple que celui-ci n'arrive pas à se mettre à jour, vous pouvez en dernier recours effectuer un cold boot.

Pour ce faire, suivez les instructions dans la page suivante : [Recovery firmware flashing](https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/userguides/recovery-mode/)

## Vérification des versions

Pour vérifier la version du firmware du crazyradio PA dongle :

```
lsusb -d 1915:7777 -v | grep bcdDevice
```

Pour vérifier la version du firmware du Crazyflie 2.0, vous avez deux options :

- Dans le menu *View*, affichez la Console Tab. Lorsque votre drone est connecté, allez dans ce nouvel onglet dans l'interface utilisateur principale et cherchez la ligne *SYS: Build*. Vous devriez trouver la date de la MAJ ainsi que son identifiant, et d'autres informations relatives au drone connecté.
- Si vous n'arrivez pas à voir cette ligne dans la Console Tab, ce qui arrive parfois, allez dans le menu *Help* puis *About*. Vous ne trouverez pas la date de la MAJ du firmware mais un autre identifiant. Si vous avez déjà un drone mis à jour, vous pouvez comparer cet identifiant afin de savoir si votre drone a la même version du firmware.

# Connecter plusieurs Crazyflie 2.0

Pour pouvoir utiliser plusieurs drones, nous utilisons la libraire cflib que nous avons déjà installée pour utiliser le cfclient. Grâce à celle-ci, nous pouvons normalement spécifier les adresses des drones auxquels nous voulons nous connecter dans le code. Pour cela, il est nécessaire de savoir comment changer l'adresse de vos drones.

## Changement d'adresse

Connectez-vous via micro-usb. Dans le menu *Connect*->*Configure 2.x*, vous pouvez modifier le channel radio, la bande passante et l'adresse.

- Channel radio : entre 0 et 125 (correspond à une fréquence entre 2400 MHz et 2525 MHz, attention avec les régulations locales sur la fréquence. Si vous utilisez une vitesse une bande passante 2M, assurez-vous d'avoir 2 channels entre chaque adresse drone utilisée (soit 2 MHz de différence)).
- Bande passante : 250K, 1M ou 2M (correspond à une vitess en kBit/s ou MBits/s. Une bande passante plus faible a plus de portée mais est plus sensible aux collisions. Si vous utilisez les drones en intérieur, préférez 1M ou 2M puisque le signal sera plus puissant).
- Adresse radio : en hexadécimal (représente pour nous l'identifiant drone).

### Avec 1 Crazyradio PA

Si l'on souhaite connecter plusieurs drones à un seul Crazyradio PA, il faut normalement modifier les adresses de manière à avoir les mêmes premiers chiffre URI, channel et bande passante, avec une adresse radio différente pour chacun des drones.

Exemple :

- radio://0/20/2M/E7E7E7E701
- radio://0/20/2M/E7E7E7E702
- radio://0/20/2M/E7E7E7E703
- radio://0/20/2M/E7E7E7E704

À savoir qu'un seul Crazyradio PA peut normalement se connecter à ~ 4 Crazyflie 2.0 en même temps.

### Avec plusieurs Crazyradio PA

De la même manière, pour connecter par exemple 2 drones par antenne, il faut avoir la même bande passante entre chaque adresse et une adresse radio différente pour chaque drone. Cependant, le premier chiffre URI et le channel doivent être les mêmes pour les drones d'une même radio.

Exemple :

- radio://0/20/2M/E7E7E7E701
- radio://0/20/2M/E7E7E7E702
- radio://1/40/2M/E7E7E7E703
- radio://1/40/2M/E7E7E7E704

Il sera peut-être aussi nécessaire de rajouter une antenne de plus pour que tous les drones puissent se connecter (ex: 5 antennes pour 4 drones).

# Utilisation d'Optitrack

## Calibration

Avant d'utiliser OptiTrack, il est nécessaire de créer une référence pour pouvoir obtenir des informations de position de nos drones qui soient correctes. 

Pour ce faire, vous pouvez suivre les instructions [ici](https://docs.optitrack.com/motive/calibration). Vous aurez besoin d'un outil de calibration OptiTrack pour cette étape.

Ensuite, dans le menu *Settings*->*Streaming* et dans *NatNet* vous pouvez changer le Up Axis à l'axe Y.

## Créer des objets à partir de marqueurs

Pour créer un objet à partir d'un set de marqueurs, vous pouvez simplement sélectionner le set de marqueurs avec la souris, puis faire un clic droit et sélectionner *Create Rigid Body*. Vous pouvez renseigner le nom de l'objet, entre autres. C'est ce nom qui sera transmis avec les informations de position, donc assurez vous d'avoir le même nom dans votre code.

## Changer la fréquence de transmission

Vous pouvez également changer la fréquence de transmission des informations. Choisissez une vitesse aux alentours de 100-120 Hz, qui corresponde à la vitesse de vos callbacks dans le code. La transmission d'information ne peut pas être plus lente que la fréquence à laquelle on essaie de la récupérer.

Pour la changer, allez dans l'onglet *Devices* et vous trouverez le champs *Camera Frame Rate*, que vous pourrez modifier.

## Activer l'option VRPN

Pour transmettre les informations, il sera nécessaire dans le menu *Settings*->*Streaming*, dans *VRPN*, d'activer l'option VRPN.

# Commandes utiles

Pour voir quels périphériques sont connectés en USB :

```
lsusb
```

# Annexes

Pour tout autre information, n'hésitez pas à parcourir les pages de [bitcraze.io](https://www.bitcraze.io/) et le [forum bitcraze](https://forum.bitcraze.io/).