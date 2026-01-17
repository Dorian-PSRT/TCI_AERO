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
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from time import sleep



mode=0      #0=simu, 1=simu et 2=Turtlesim
autostart=True  #lance automatiquement les nodes
build=True

# Dossiers
dossier = Path(__file__).parent #dossier du script
nodes_dir = "fusion_CP_Consensus"
workspace_path = dossier.parents[1]

# fichiers
liste_fichiers = ["global_path_node","local_path_node","decision_node"]  #,"my_robot_driver_node"
setup_file = dossier / 'setup.py'
launch_file = dossier / "launch/essaim_launch.yaml"

# Utils.json
utils = dossier/"utils.json" 
with open(utils) as f:
    file = json.load(f)


nb_drones=file["nb_drones"]
mode=int(file["mode"])

for id in range (2,5+1):  #5 = nombre max de drones
    for fichier in liste_fichiers:
        source = dossier / nodes_dir / f"{fichier}1.py"
        destination = dossier / nodes_dir / f"{fichier}{id}.py"
        if destination.exists():
            os.remove(destination)
        if id <= nb_drones:
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

if mode != 2:
    static_nodes.pop(0)     #enlève les nodes liées à turtlesim inutiles à la simu
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

ws_simu=workspace_path.parent/"ws_simu"

os.chdir(ws_simu)
if build:
    try:
        # Exécuter la commande colcon build
        subprocess.run(['colcon', 'build','--packages-skip-regex', 'webots_ros2.*'], check=True)
        print("✅ colcon build simu réussi")
    except subprocess.CalledProcessError as e:
        print(f"❌ Une erreur est survenue lors de l'exécution de colcon build: {e}")


titre_terminal = "TEMP_ne_pas_fermer"


terminal_type="gnome-terminal"



def open_terminal(*cmd):
    full_cmd = (
        f"source {workspace_path}/install/setup.bash; "  #f"source ~/Desktop/TCI_AERO/ws_drones/install/setup.bash; " 
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
    # if os.path.exists(utils):
    #     file = json.load(open(utils))



if autostart:
    #close_old_terminals()
    subprocess.run(["pkill", "-f", terminal_type], check=False)
    

    if mode :
        open_terminal("ros2", "launch", "crazyflie_control", "launch.py")
        sleep(5)
        input("Appuie sur Entrée si ça a fini d'init.")
        open_terminal("ros2", "launch", "crazyflie_control", "takeoff.launch.py")
        open_terminal("ros2", "run", "my_package", "interface_node_real")
        sleep(5)

        input("Appuie sur Entrée pour lancer les nodes.")

        open_terminal("ros2", "run", "tortues", "observer")
        open_terminal("ros2", "launch", "fusion_CP_Consensus", "essaim_launch.yaml")
        
        input("Appuie sur Entrée pour LAND.")

        for i in range(1,5):
            subprocess.Popen(
            ["ros2", "service", "call", f"/crazyflie_{i}/land", "std_srvs/srv/Trigger"]
            )

        sleep(5)

        subprocess.run(["pkill", "-f", terminal_type], check=False)
    else:
        open_terminal("ros2", "launch", "my_package", "robot_launch.py")
        open_terminal("ros2", "run", "my_package", "interface_node")
        sleep(8)
        open_terminal("ros2", "run", "tortues", "observer")
        open_terminal("ros2", "launch", "fusion_CP_Consensus", "essaim_launch.yaml")
        input("Appuie sur Entrée pour KILL.")
        subprocess.run(["pkill", "-f", terminal_type], check=False)


# def load_config():
#     """Charge mode et nb_drones depuis utils.json sans toucher aux autres données."""
#     if utils_file.exists():
#         try:
#             with open(utils_file, "r") as f:
#                 data = json.load(f)
#         except:
#             data = {}
#     else:
#         data = {}

#     return {
#         "mode": int(data.get("mode", 0)),
#         "nb_drones": int(data.get("nb_drones", 1)),
#         "full": data  # garde tout le fichier
#     }


# def save_config(mode, nb_drones, full_data):
#     """Met à jour UNIQUEMENT mode et nb_drones dans le JSON."""
#     full_data["mode"] = int(mode)
#     full_data["nb_drones"] = int(nb_drones)

#     with open(utils_file, "w") as f:
#         json.dump(full_data, f, indent=4)


# # ------------------------------------------------------------
# #  ROS2 async runner
# # ------------------------------------------------------------

# def run_cmd_async(cmd, log_widget):
#     def run():
#         log_widget.insert(tk.END, f"> {cmd}\n")
#         log_widget.see(tk.END)

#         process = subprocess.Popen(
#             ["bash", "-c", f"{setup_bash}; {cmd}"],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.STDOUT,
#             text=True
#         )

#         for line in process.stdout:
#             log_widget.insert(tk.END, line)
#             log_widget.see(tk.END)

#     threading.Thread(target=run, daemon=True).start()


# # ------------------------------------------------------------
# #  INTERFACE
# # ------------------------------------------------------------

# root = tk.Tk()
# root.title("Interface Essaim - Contrôle")

# # Charger configuration existante
# cfg = load_config()
# full_json_data = cfg["full"]


# # ----------------------- ZONE LOGS -------------------------

# log = scrolledtext.ScrolledText(root, width=80, height=22)
# log.pack(padx=10, pady=10)


# # --------------------- CADRE PARAMÈTRES ---------------------

# frame_params = ttk.LabelFrame(root, text="Paramètres")
# frame_params.pack(fill="x", padx=10, pady=5)

# # Mode
# mode_var = tk.IntVar(value=cfg["mode"])
# tk.Label(frame_params, text="Mode :").grid(row=0, column=0, padx=5, pady=5, sticky="w")

# tk.Radiobutton(frame_params, text="Simulation", variable=mode_var, value=0)\
#     .grid(row=0, column=1, sticky="w", padx=10)

# tk.Radiobutton(frame_params, text="Réel", variable=mode_var, value=1)\
#     .grid(row=0, column=2, sticky="w", padx=10)

# # Nombre de drones
# tk.Label(frame_params, text="Nombre de drones :").grid(row=1, column=0, padx=5, pady=5, sticky="w")

# nb_drones_var = tk.StringVar(value=str(cfg["nb_drones"]))
# tk.Entry(frame_params, textvariable=nb_drones_var, width=10)\
#     .grid(row=1, column=1, sticky="w", padx=10)

# # Bouton validation
# def valider_parametres():
#     """Valide les paramètres, met à jour le JSON et active les boutons ROS."""
#     try:
#         nb = int(nb_drones_var.get())
#         if nb < 1:
#             raise ValueError
#     except ValueError:
#         log.insert(tk.END, "[ERREUR] Le nombre de drones doit être un entier >= 1\n")
#         log.see(tk.END)
#         return

#     # Sauvegarde JSON
#     save_config(mode_var.get(), nb, full_json_data)

#     log.insert(tk.END,
#                f"\n✔ Paramètres validés :\n"
#                f"  → Mode = {mode_var.get()}\n"
#                f"  → nb_drones = {nb}\n\n")
#     log.see(tk.END)

#     # Désactiver réglages
#     for w in widgets_params:
#         w.config(state="disabled")

#     # Activer boutons ROS
#     for b in boutons_ros:
#         b.config(state="normal")


# btn_valider = tk.Button(frame_params, text="Valider", bg="#ccffcc",
#                         command=valider_parametres)
# btn_valider.grid(row=1, column=2, padx=10)


# # Liste des widgets paramètre pour désactivation ultérieure
# widgets_params = frame_params.winfo_children()


# # ------------------------- BOUTONS ROS -----------------------

# frame_actions = ttk.LabelFrame(root, text="Actions")
# frame_actions.pack(fill="x", padx=10, pady=10)

# def init_system():
#     run_cmd_async("ros2 launch crazyflie_control launch.py", log)

# def takeoff():
#     run_cmd_async("ros2 launch crazyflie_control takeoff.launch.py", log)

# def lancer_nodes():
#     run_cmd_async("ros2 run tortues observer", log)
#     run_cmd_async("ros2 launch fusion_CP_Consensus essaim_launch.yaml", log)

# def land():
#     nb = int(nb_drones_var.get())
#     for i in range(1, nb + 1):
#         run_cmd_async(f"ros2 service call /crazyflie_{i}/land std_srvs/srv/Trigger", log)

# def kill_all():
#     run_cmd_async("pkill -f ros2", log)


# # Création boutons (désactivés par défaut)
# boutons_ros = []

# def add_button(text, callback, row, col, w=25, h=1, bg="white", fg="black", span=1):
#     b = tk.Button(frame_actions, text=text, width=w, height=h,
#                   command=callback, bg=bg, fg=fg, state="disabled")
#     b.grid(row=row, column=col, padx=10, pady=5, rowspan=span)
#     boutons_ros.append(b)


# add_button("1. Initialisation", init_system, 0, 0)
# add_button("2. Décollage", takeoff, 1, 0)
# add_button("3. Action", lancer_nodes, 2, 0)
# add_button("ATTERISSAGE", land, 0, 1, w=20, h=3, bg="lightgreen", span=3)
# add_button("KILL", kill_all, 0, 2, w=20, h=3, bg="red", fg="white", span=3)

# root.mainloop()
