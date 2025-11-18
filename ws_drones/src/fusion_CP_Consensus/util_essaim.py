##################################
# 
# 
# 
# 
# 
#  il s'occupe de tout :)
# 
# 
# 
# 
#
##################################

from pathlib import Path
import shutil
import re
import os
import yaml
import json, signal
import subprocess
from time import sleep
import cflib.crtp



mode=2      #0=Turtlesim, 1=simu et 2=réel
autostart=True  #lance automatiquement les nodes
build=True
radio=True

# Dossiers
dossier = Path(__file__).parent #dossier du script
nodes_dir = "fusion_CP_Consensus"
workspace_path = dossier.parents[1]
workspace_path2 = dossier.parents[2] / "ws_crazyDev"

# fichiers
liste_fichiers = ["global_path_node","local_path_node","control_node","decision_node"]  #,"my_robot_driver_node"
setup_file = dossier / 'setup.py'
launch_file = dossier / "launch/essaim_launch.yaml"

# radio
uris=[]
cflib.crtp.init_drivers()
available = cflib.crtp.scan_interfaces()
for i in available:
    uris.append(i[0])
    print("Interface with URI [%s] found and name/comment [%s]" % (i[0], i[1]))


# Utils.json
utils = dossier/"utils.json" 
with open(utils) as f:
    file = json.load(f)

nb_drones=file["nb_drones"]

file["uri"]=uris

with open(utils, "w") as outfile:
    json.dump(file, outfile, indent=4)

for id in range (2,nb_drones+1):
    for fichier in liste_fichiers:
        source = dossier / nodes_dir / f"{fichier}1.py"
        destination = dossier / nodes_dir / f"{fichier}{id}.py"
        if destination.exists():
            os.remove(destination)
        shutil.copy(source, destination)
        print(f"✅ Copié : {source.name} → {destination.name}")





node_files = [f for f in os.listdir(dossier / nodes_dir) if f.endswith('.py') and 'node' in f]
node_files = sorted(node_files,reverse=True)

# Génère la liste de lignes console_scripts
new_console_scripts = [
    f"'{os.path.splitext(f)[0]} = {nodes_dir}.{os.path.splitext(f)[0]}:main',"
    for f in node_files
]

# Lecture du fichier setup.py
with open(setup_file, 'r') as f:
    content = f.read()

# Remplace la section console_scripts
# Ici on assume que la section commence par 'console_scripts': [ et se termine par ],
pattern = re.compile(
    r"(entry_points\s*=\s*{[^}]*'console_scripts'\s*:\s*\[)(.*?)(\]\s*[,}])",
    re.DOTALL
)

new_content = pattern.sub(
    lambda m: m.group(1) + '\n    ' + '\n    '.join(new_console_scripts) + '\n' + m.group(3),
    content
)

# Écrit le fichier setup.py modifié
with open(setup_file, 'w') as f:
    f.write(new_content)

print("✅ setup.py mis à jour avec les nodes actuels.")



# Nodes existants à ignorer ou à conserver (par exemple turtlesim)
static_nodes = [
    {
        'node': {
            'pkg': 'turtlesim',
            'exec': 'turtlesim_node',
            'name': 'sim',
            'namespace': ''
    }},
    {   'node': {
            'pkg': "tortues",
            'exec': "spawn",
            'name': "apparition",
            'namespace': ""
    }},
    {   'node': {
            'pkg': "fusion_CP_Consensus",
            'exec': "fake_ot_node",
            'name': "fake_ot_node",
            'namespace': ""
    }}
]

if mode == 1:
    static_nodes.pop(0)     #enlève les nodes liées à turtlesim inutiles à la simu
    static_nodes.pop(0)
elif mode == 2:
    static_nodes.pop(0)
    static_nodes.pop(0)
    static_nodes.pop(0)

# Génère la liste des nodes dynamiques
dynamic_nodes = [
    {
        'node': {
            'pkg': 'fusion_CP_Consensus',
            'exec': os.path.splitext(f)[0],
            'name': os.path.splitext(f)[0],
            'namespace': ''
    }
    }
    for f in node_files
]

# Combine static et dynamic
all_nodes = static_nodes + dynamic_nodes

# Structure finale YAML
launch_dict = {'launch': all_nodes}

# Écrit le fichier YAML
with open(launch_file, 'w') as f:
    yaml.dump(launch_dict, f, sort_keys=False)

print(f"✅ {launch_file} mis à jour avec {len(dynamic_nodes)} nodes dynamiques.")



os.chdir(workspace_path)
if build:
    try:
        # Exécuter la commande colcon build
        subprocess.run(['colcon', 'build'], check=True)
        print("✅ colcon build réussi")
    except subprocess.CalledProcessError as e:
        print(f"❌ Une erreur est survenue lors de l'exécution de colcon build: {e}")



titre_terminal = "TEMP_ne_pas_fermer"

terminal_type="gnome-terminal"

def open_terminal(*cmd,ws):
    full_cmd = (
        f"source {ws}/install/setup.bash; "  #f"source ~/Desktop/TCI_AERO/ws_drones/install/setup.bash; " 
        + " ".join(cmd)
        + "; exec bash"
    )

    subprocess.Popen([
        terminal_type,
        "--title", titre_terminal,
        "--",
        "bash", "-c", full_cmd
    ])
    #proc = subprocess.Popen([terminal_type,"--title", titre_terminal, "--", *cmd])
    if os.path.exists(utils):
        file = json.load(open(utils))



if autostart:
    #close_old_terminals()
    subprocess.run(["pkill", "-f", terminal_type], check=False)
    #open_terminal("ros2", "run", "crazyflie", "Control_node.py")
    open_terminal("ros2", "run", "crflie_test", "Mocap_node",ws=workspace_path2)
    open_terminal("ros2", "run", "crazyflie", "interface_node_vrai",ws=workspace_path)
    sleep(2)

    # open_terminal("ros2", "run", "tortues", "observer")
    #open_terminal("ros2", "launch", "fusion_CP_Consensus", "essaim_launch.yaml",ws=workspace_path)

    open_terminal("rqt_graph")


    #les messages "# Failed to use specified server: ..." ne sont pas inquiétants, ce n'est pas bloquant

