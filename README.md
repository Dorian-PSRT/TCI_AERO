# Tutoriel
## Organisation du dépôt
Bienvenue sur le dépôt de la promo AERO-TCI 2026.
Vous êtes sur la branche main qui rassemble toutes les informations et documents du projet.

 - [Informations et documents](https://github.com/Dorian-PSRT/TCI_AERO/tree/main/Informations%20et%20documents "Informations et documents") est mis à jour avec la documentation du projet.
 - [Nouveau dossier](https://github.com/Dorian-PSRT/TCI_AERO/tree/main/Nouveau%20dossier "Nouveau dossier") contient les archives de code.

Les autres branches ont permis d'avancer sur le projet sur 3 axes principaux :

 - [develop](https://github.com/Dorian-PSRT/TCI_AERO/tree/develop "develop") a servi à créer des fonctions en les testant sur TurtleSim 
 - [simulateur](https://github.com/Dorian-PSRT/TCI_AERO/tree/simulateur "simulateur ") a d'abord été dédié au tests sur simulateur puis l'ensemble du code y a été regroupé
 - [crazyflie](https://github.com/Dorian-PSRT/TCI_AERO/tree/crazyflie "crazyflie") a servi à apprendre à contrôler les drones 

## Présentation de l'ensemble du projet
 Ce projet avait pour but de participer au drone défense hackathon, qui a eu lieu entre le 24 octobre et le 24 novembre (phase préliminaire incluse), nous avons dû nous pencher sur la création d’un scénario ainsi que la programmation d’un essaim de drone collaboratif capable de le réaliser. Ce [scénario](https://github.com/Dorian-PSRT/TCI_AERO/blob/main/Informations%20et%20documents/Fil_rouge_projet.md "main/Information et documents/ Fil_rouge_projet.md") devait nous permettre de démontrer le côté collaboratif de notre essaim, ainsi que d’être le plus complet possible pour avoir une chance d’être sélectionné par le jury.
 
## Ressources Optitrack
[Clara]
## Ressources Crazyflie
[Tutoriel Crazyflie 2.0](https://github.com/Dorian-PSRT/TCI_AERO/tree/main/Informations%20et%20documents/Tutoriel%20Crazyflie%202.0.md) contient un tutoriel sur la prise en main des Crazyflie 2.0 et d'OptiTrack.
## Détails du code

### Lancer le programme

Pour cela rendez vous sur la branche [simulateur](https://github.com/Dorian-PSRT/TCI_AERO/tree/simulateur "simulateur ") afin d'avoir les dernières fonctionnalités développées.
Dans un premier temps choisissez les paramètres en modifiant le fichier *utils.json* dans le package *fusion_CP_Consensus*du workspace *ws_drones*. 
Chemin complet : TCI_AERO\ws_drones\src\fusion_CP_Consensus\utils.json

		{
			"nb_drones": 4,		# à modifier selon le nombre de drones souhaité
			"mode": 0,			# 0 pour lancer le simulateur ou 1 pour des drones réels
			"obstacles": [		# créations d'obstacles virtuels, 3 valeurs par obstacle
				[
					0.0,		# position en x de l'obstacle
					0.0,		# position en y de l'obstacle
					2.0			# rayon de l'obstacle
				],
				[
					2.0,
					2.0,
					1.5
				],
				[
					0.5,
					5.0,
					0.25
				],
				[
					-0.5,
					5.0,
					0.25
				]
			]
		}

Il ne reste plus qu'à lancer le fichier *util_essaim.py* qui automatise toute les actions nécéssaires pour faire fonctionner l'essaim. 
Chemin complet : TCI_AERO\ws_drones\src\fusion_CP_Consensus\util_essaim.py

 Si vous lancer le programme avec des drones réels :

 1. Vérifiez que l'initialisation s'est bien passée (drone connectés, pas de messages d'erreur,...) puis appuyez sur "Entrée" pour donner la consigne de décollage.
 2. Assurez-vous que tous les drones sont stabilisés en vol puis appuyez à nouveau sur "Entrée" pour lancer le scénario.
 3. A tout moment vous pouvez appuyer un troisième fois sur "Entrée" pour faire atterir les drones.



### Contenu du code
Afin de faciliter l'interprétation chaque programme est commenté.
Les types de messages et services ROS2 personnalisés sont définis dans le dossier *my_custom_interfaces*du workspace *ws_drones* 
Chemin complet : TCI_AERO\ws_drones\src\my_custom_interfaces

Pour mieux comprendre l'achitecture globale vous trouverez le [rqt_graph](https://github.com/Dorian-PSRT/TCI_AERO/blob/main/Informations%20et%20documents/rqt_graph_3drones_simu.png) correspondant dans le dossier *Informations et documents* de la branche *main*.
<!--stackedit_data:
eyJoaXN0b3J5IjpbODA1MTExODU1LDE3MjcyNDM1NTldfQ==
-->
