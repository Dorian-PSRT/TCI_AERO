# Liens des ressources principales

 - [Règlement du Challenge - Agorize](https://www.agorize.com/fr/challenges/drone-defense-hackathon/agreements?lang=fr)
 - [Documentation du matériel mis à disposition - Agorize](https://www.agorize.com/fr/challenges/drone-defense-hackathon/pages/materiel?lang=fr)
 - [Discord du Challenge](https://discord.gg/Qwb9c3cZ)
-  [ Lien d'accès pour Google Drive vers les documents utiles](https://cas5-0-urlprotect.trendmicro.com/wis/clicktime/v1/query?url=https://drive.google.com/drive/folders/1W_Wg2FVmQdwj2N79XSCobN0JTkpTJQo7?usp=drive_link&umid=1f2e17b0-60fb-439a-a2c8-c74d0f593a5c&rct=1761678757&auth=30c0fd8b430f5bbfd67a3bd83277817e276e0b55-e367aca922b926490718f84849ca771e0c325020) (pas encore accepté ??)
-   Un lien d'accès pour Google Drive vers le dossier de l'équipe pour partager des documents et  déposer le pitch final le 3e jour du hackathon (pas trouvé ??)

# Actualités de l'équipe
## Compte rendu du mercredi 29/10/2025

### Résumé de session d' "Onboarding" de la veille
[Formulaire pour restrictions alimentaires et logistique](https://cas5-0-urlprotect.trendmicro.com/wis/clicktime/v1/query?url=https://docs.google.com/forms/d/e/1FAIpQLSd2zwAvCWwnV72xIpKt66rNMgGJJnAYXtg2zbn6CrX4VLlAxA/viewform?usp=sharing&ouid=106816409187166232513&umid=1f2e17b0-60fb-439a-a2c8-c74d0f593a5c&rct=1761678757&auth=30c0fd8b430f5bbfd67a3bd83277817e276e0b55-37fa0f3144ecc5d58fdbd04a89eda0a3b845b4b4)

Quelle est la philosophie des organisateur concernant la réutilisation de modèles externes repris pour l'application étudiée ? ==> Réponse : Lire le règlement, mais si on utilise des ressources libres de droits c'est ok

Entreprises affiliées au Challenge 2 : [Naval Group](https://www.naval-group.com/en/drones), [Delair](https://delair.aero/), [Thales](https://www.thalesgroup.com/fr/catalogue-de-solutions/defense/les-drones-au-coeur-du-combat), [Cerbair](https://www.cerbair.com/)

### Réunion de lancement réel du projet
Conseils de F. Khenfri :
Travailler en petits groupes (CrazyFly physique, CrazyFly simulateur, Nodes)
Première chose à faire pour ceux qui utilisent le simulateur 

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

 - [x] Max Consensus + Launch control (Di)
 - [ ] Méthodes de navigation , ex : Model Predict Control (A)
 - [x] Zoom sur méthode des champs potentiels (Do)
 - [ ] Planification de trajectoire avec plusieurs drones,  ex : faisabilité Champs Potentiels ? (N)
 - [x] Fonction Score ( C )
 - [x] Recherches globales (M)

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

 - [x] Précision sur le matériel
 - [x] Est-ce que les drones pourront voler ?
 - [x] Est-ce qu’on peut ramener un cerceau avec des marqueurs Optitrack par exemple ?
 - [ ] Est-ce qu’on casse une fenêtre ?
 - [ ] C’est quoi le simulateur ?
 - [ ] Est-ce qu’on peut inviter des externes ? ==> A première vue, non.
       A confirmer
 - [x] Quelle est la philosophie des organisateur concernant la
       réutilisation de modèles externes repris pour l'application
       étudiée ? ==> Lire le règlement, mais si on utilise des
       ressources libres de droits c'est ok

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTkyOTA3MDI1NCwtNjQ3NzM2Mzg2LC0xMj
kzNzI3ODk5LDk4ODA3ODEwNSwtMTY3OTQyMzU5MSwzMTUyNDIz
OTUsMjA2MzAwMjc4NCwtMTkxNzg5MzU4MywtMTM0ODg4ODI1Ny
wyMTI4NzkwODc4LDQwMzY2MzEwLC0xNTIyODU0MDk4LC0xNzk0
NjczNzg4LC05MzYxMTg2MjMsMTI5ODk0MTA4OSwtMTM1MjM1ND
UwXX0=
-->