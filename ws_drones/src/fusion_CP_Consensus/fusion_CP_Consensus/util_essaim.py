##################################
# 
# 
# 
# 
# 
#  à n'exécuter qu'une fois 
# 
# 
# 
# 
#
##################################

from pathlib import Path
import shutil

nb_drones=4

# Dossier courant du script
dossier = Path(__file__).parent
liste_fichiers = ["global_path_node","local_path_node","pid_control_node"]

for id in range (2,nb_drones+1):
    for fichier in liste_fichiers:
        source = dossier / f"{fichier}1.py"
        destination = dossier / f"{fichier}{id}.py"
        #shutil.copy(source, destination)
        print(f"✅ Copié : {source.name} → {destination.name}")