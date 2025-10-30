# Liens des ressources principales :school_satchel:

 - [Règlement du Challenge - Agorize](https://www.agorize.com/fr/challenges/drone-defense-hackathon/agreements?lang=fr)
 - [Documentation du matériel mis à disposition - Agorize](https://www.agorize.com/fr/challenges/drone-defense-hackathon/pages/materiel?lang=fr)
 - [Discord du Challenge](https://discord.gg/Qwb9c3cZ)
-  [ Lien d'accès pour Google Drive vers les documents utiles](https://cas5-0-urlprotect.trendmicro.com/wis/clicktime/v1/query?url=https://drive.google.com/drive/folders/1W_Wg2FVmQdwj2N79XSCobN0JTkpTJQo7?usp=drive_link&umid=1f2e17b0-60fb-439a-a2c8-c74d0f593a5c&rct=1761678757&auth=30c0fd8b430f5bbfd67a3bd83277817e276e0b55-e367aca922b926490718f84849ca771e0c325020) 
-   Un lien d'accès pour Google Drive vers le dossier de l'équipe pour partager des documents et  déposer le pitch final le 3e jour du hackathon (à ajouter par ceux qui ont l'accès)
- 
### Ressources complémentaires

- [Informations sur l'imprimante 3D](https://www.cosmyx3d.com/imprimante-3d-nova) dimension : **300x200x270 mm**  (*note*: plus d'informations et fiche technique sur le [Drive](https://drive.google.com/drive/folders/12A98-17QO9h9z6vLt7dqGft_knDHMLwn))
- ligne de commande pour lancer le simulateur : **ros2 launch webots_ros2_crazyflie robot_launch.py**

# Actualités de l'équipe :tropical_fish:
## Compte rendu du jeudi 30/10/2025 :turtle:

### Missions du jour :
 - Equipe simulation - Objectif : Créer plusieurs CrazyFly et mettre en place le premier scénario [Al + Ma]
 - Equipe CrazyFly - Objectif : Se renseigner sur le matériel fourni + Contrôler le drone [Cl + Na]
 - Equipe nodes - Objectif : Fichier launch complet + classe pour calcul des champs potentiels [Di +Do]

### Réunion à 17h : 

## Compte rendu du mercredi 29/10/2025 :partly_sunny:

### Résumé de session d' "Onboarding" de la veille
[Formulaire pour restrictions alimentaires et logistique](https://cas5-0-urlprotect.trendmicro.com/wis/clicktime/v1/query?url=https://docs.google.com/forms/d/e/1FAIpQLSd2zwAvCWwnV72xIpKt66rNMgGJJnAYXtg2zbn6CrX4VLlAxA/viewform?usp=sharing&ouid=106816409187166232513&umid=1f2e17b0-60fb-439a-a2c8-c74d0f593a5c&rct=1761678757&auth=30c0fd8b430f5bbfd67a3bd83277817e276e0b55-37fa0f3144ecc5d58fdbd04a89eda0a3b845b4b4)

Quelle est la philosophie des organisateur concernant la réutilisation de modèles externes repris pour l'application étudiée ? ==> Réponse : Lire le règlement, mais si on utilise des ressources libres de droits c'est ok

Entreprises affiliées au Challenge 2 : [Naval Group](https://www.naval-group.com/en/drones), [Delair](https://delair.aero/), [Thales](https://www.thalesgroup.com/fr/catalogue-de-solutions/defense/les-drones-au-coeur-du-combat), [Cerbair](https://www.cerbair.com/)

### Réunion de lancement réel du projet
Conseils de F. Khenfri :
Travailler en duo (CrazyFly physique, CrazyFly simulateur, Nodes)
Première chose à faire pour ceux qui utilisent le simulateur, essayer de déplacer le drone

On a deux disques durs à disposition pour utiliser Ubuntu sur des ordinateurs personnels

**Si on fait une bonne performance , qu'on est très impliqués pour la réussite du projet ; après le 26 novembre c'est VACANCES !!!**

#### Challenge 2: Coopérer pour réussir (Note sur 20, 5 points par critère)

 -   Efficacité de la coordination collective: Capacité des drones à travailler ensemble sans heurts (couverture optimale, rapidité d’exécution, absence de collisions).
            
  -   Originalité et pertinence du cas d’usage: Qualité et créativité du scénario imaginé (mission militaire, surveillance, sécurité civile, etc.).
            
    -   Capacité d’actions successives: Aptitude à enchaîner plusieurs actions coordonnées avec ou sans intervention humaine.
            
  -   Nombre de défis atteints: Évaluation du nombre de sous-défis relevés avec succès par l’équipe, en plus de la qualité de leur réalisation.
  
##  To Do List :bell:
  
 - [ ] Message friendly Discord (pour teams et mentors challenge 2) [Do]
 - [ ] Remplir le formulaire [Tous]
 - [ ] Ajouter lien Google Drive pour dépôt du pitch  [N, C ou A]
 - [ ] Recréer support Motive Optitrack Deck dans la liste du matériel pour pouvoir l'imprimer ici [M]
 - [ ] Etat de l'art plus poussé

## Compte rendu du mardi 28/10/2025 :earth_africa:

### Méthode des champs potentiels (Do)
[Lien vidéo plannification de chemin d'un robot par champs potentiels](https://youtu.be/FT5DQ-SGYL4?t=1675)

[Explication des limites de la méthode : minima locaux](https://medium.com/@rymshasiddiqui/path-planning-using-potential-field-algorithm-a30ad12bdb08)

### Autres méthodes de navigation (A)
#### ORCA

These pour l evitement individuelle des obstacles pour les drones + plannification route. (centralisé vs décentralisé)
https://www.sesarju.eu/sites/default/files/documents/sid/2024/papers/SIDs_2024_paper_059%20final.pdf

Explication de la methode avec un ROS + simu. 
https://arxiv.org/html/2508.06722v1

#### Model Predictive Control

Algorithme mathématique sur la MPC pour un essaim. 
https://www.researchgate.net/publication/352277057_Model_predictive_control_for_path_planning_of_UAV_group
https://aerial-core.eu/wp-content/uploads/2021/11/Distributed_Predictive_Drone_Swarms_in_Cluttered_E.pd


git mpc ou drone passe par des portes: Drone Navigation Through Moving Gates Using Model Predictive Control https://github.com/guilherme-mertens/drone-model-predictive-control

git avec code (pas mpc) d'un challenge. Crazyfly doit identifier et passer a travers des "portes" https://github.com/utiasDSL/safe-control-gym/tree/beta-iros-competition


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

Lien état de l’art planification des trajectoires : https://www.ferdinandpiette.com/blog/2011/05/algorithmes-de-planification-de-trajectoires-bref-etat-de-lart/

Lien Thèse de calcul dynamique de chemin (appliqué aux essaims) : https://theses.hal.science/tel-02500580v1/file/FALOMIR-BAGDASSARIAN_EMA_2019.pdf

Cette thèse utilise dans un premier temps la méthode des champs potentielle pour calculer la trajectoire d’un seul drone puis l’applique à un essaim. 

L’espace qui entoure le drone est décomposé en maille et le potentiel est calculé pour chaque maille. Ici cette méthode est principalement utilisée pour que le drone se déplace dans un milieu inconnu et atteigne un pt en évitant les obstacles qu’il détecte sur son chemin. 

Appliqué à l’essaim, lors du calcul de la trajectoire la position des autres drones sera aussi prise en compte. 

Les autres drones sont considérés comme des obstacles. 


## Séance projet du mardi 28/10/2025 :

Chacun fait l’**état de l’art** d’un sujet et **présente** les détails et les potentielles couches de difficultés **à 11h.**

 - [x] Max Consensus + Launch control (Di)
 - [x] Méthodes de navigation , ex : Model Predict Control (A)
 - [x] Zoom sur méthode des champs potentiels (Do)
 - [x] Planification de trajectoire avec plusieurs drones,  ex : faisabilité Champs Potentiels ? (N)
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
eyJoaXN0b3J5IjpbLTEzOTk4MjY4MzAsLTQ2MjM2NTYxNiwtNj
Q3NzM2Mzg2LC0xMjkzNzI3ODk5LDk4ODA3ODEwNSwtMTY3OTQy
MzU5MSwzMTUyNDIzOTUsMjA2MzAwMjc4NCwtMTkxNzg5MzU4My
wtMTM0ODg4ODI1NywyMTI4NzkwODc4LDQwMzY2MzEwLC0xNTIy
ODU0MDk4LC0xNzk0NjczNzg4LC05MzYxMTg2MjMsMTI5ODk0MT
A4OSwtMTM1MjM1NDUwXX0=
-->