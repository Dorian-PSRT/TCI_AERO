# Actualités de l'équipe

## Compte rendu du mardi 28/10/2025 :


Demander disques durs SSD pour Linux à F. Khenfri ==> Réponse : Demander au service Info

### Méthode des champs potentiels (Do)
[Lien vidéo plannification de chemin d'un robot par champs potentiels](https://youtu.be/FT5DQ-SGYL4?t=1675)

[Explication des limites de la méthode : minima locaux](https://medium.com/@rymshasiddiqui/path-planning-using-potential-field-algorithm-a30ad12bdb08)

### Autres méthodes de navigation (A)
#### ORCA
m
#### Model Predictive Control

### Launch File (Di)
[tuto Launch file](https://docs.ros.org/en/foxy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html)
Ce lien est un tutoriel pour créer un launch file et comment l'utiliser. Il permet de lancer plusieurs node en même temps avec une seule ligne de commande.
Travailler avec un launch file nous facilitera la vie lors de nos tests.

**Bonus :** Collecte de données
A terme il serait intéressant de développer un "observateur" qui va collecter toutes les informations échangées lors du test, pour les traiter et en faire des **jolies graphiques**.

Lien bonus: [thèse intéressante sur l'utilisation de Consensus avec un essaim de drones](https://theses.hal.science/tel-02529658/document)

### Etat de l'art essaims décentralisés (M)
Algorithme de fusion des données décentralisé
https://www.sciencedirect.com/science/article/pii/S0957417423019462?ref=pdf_download&fr=RR-2&rr=9959d4e4dd7dd652

Apprentissage par reforcement du controle d'un essaim de drone
https://arxiv.org/pdf/2109.07735

Algorithme robuste d'atribution des taches
https://dspace.mit.edu/handle/1721.1/42177

Code de controle d'essaim de drone basé sur la dépense d'energie 
https://www.sciencedirect.com/science/article/pii/S0968090X23003777#sec4

### Score ( C )
"UAV Swarm Mission Planning in Dynamic Environment Using Consensus-Based Bundle Algorithm" (2020) calcul d'une fonction score avec max-plus
   score/état/valeur ? weighted score ?
   "Max-consensus of multi-agent systems in random networks" (2024) pas encore lu mais a l'air intéressant

### Planification de trajectoire à plusieurs drones (N)




## Séance projet du mardi 28/10/2025 :

Chacun fait l’**état de l’art** d’un sujet et **présente** les détails et les potentielles couches de difficultés **à 11h.**

 - Max Consensus + Launch control (Di)
 - Méthodes de navigation , ex : Model Predict Control (A)
 - Zoom sur méthode des champs potentiels (Do)
 - Planification de trajectoire avec plusieurs drones,  ex : faisabilité
   Champs Potentiels ? (N)
 - Fonction Score ( C )
   "UAV Swarm Mission Planning in Dynamic Environment Using Consensus-Based Bundle Algorithm" (2020) calcul d'une fonction score avec max-plus
   score/état/valeur ? weighted score ?
   "Max-consensus of multi-agent systems in random networks" (2024) pas encore lu mais a l'air intéressant
 - Recherches globales (M)

## Compte rendu du lundi 27/10/2025 :
**Tempête d'idées :**

405 h de projet (hors Grand Palais) soit environt 70 h par personnes

On pourrait télécharger ROS2 sur un disque dur externe.

Pour les prochains jours, prévoir la direction de notre projet et nos ambitions techniques

Les 3 jours au GP : Comment on y va ? C’est payé par l’école ? Où est-ce qu’on loge ?

**Propositions de travaux dans un futur proche :**

 - Etat de l’art [anticollision]
 - Etat de l’art [score]
 - Redémarrage du max consensus une fois que le drone précédent a fait
   sa mission

**Questions pour les organisateurs :**

 1. Précision sur le matériel
 2. Est-ce que les drones pourront voler ?
 3. Est-ce qu’on peut ramener un cerceau avec des marqueurs Optitrack
    par exemple ?
 4. Est-ce qu’on casse une fenêtre ?
 5. C’est quoi le simulateur ?
 6. Est-ce qu’on peut inviter des externes ?
 7. Quelle est la philosophie des organisateur concernant la réutilisation de modèles externes repris pour l'application étudiée ?

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTMyNDcxNjU3NywyMDYzMDAyNzg0LC0xOT
E3ODkzNTgzLC0xMzQ4ODg4MjU3LDIxMjg3OTA4NzgsNDAzNjYz
MTAsLTE1MjI4NTQwOTgsLTE3OTQ2NzM3ODgsLTkzNjExODYyMy
wxMjk4OTQxMDg5LC0xMzUyMzU0NTBdfQ==
-->