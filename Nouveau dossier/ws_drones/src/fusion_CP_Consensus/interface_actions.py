import subprocess
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from pathlib import Path
import json

workspace_path = Path(__file__).parents[1]
utils_file = Path(__file__).parent / "utils.json"

setup_bash = f"source {workspace_path}/install/setup.bash"


# ------------------------------------------------------------
#  JSON : Chargement / Sauvegarde
# ------------------------------------------------------------

def load_config():
    """Charge mode et nb_drones depuis utils.json sans toucher aux autres données."""
    if utils_file.exists():
        try:
            with open(utils_file, "r") as f:
                data = json.load(f)
        except:
            data = {}
    else:
        data = {}

    return {
        "mode": int(data.get("mode", 0)),
        "nb_drones": int(data.get("nb_drones", 1)),
        "full": data  # garde tout le fichier
    }


def save_config(mode, nb_drones, full_data):
    """Met à jour UNIQUEMENT mode et nb_drones dans le JSON."""
    full_data["mode"] = int(mode)
    full_data["nb_drones"] = int(nb_drones)

    with open(utils_file, "w") as f:
        json.dump(full_data, f, indent=4)


# ------------------------------------------------------------
#  ROS2 async runner
# ------------------------------------------------------------

def run_cmd_async(cmd, log_widget):
    def run():
        log_widget.insert(tk.END, f"> {cmd}\n")
        log_widget.see(tk.END)

        process = subprocess.Popen(
            ["bash", "-c", f"{setup_bash}; {cmd}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            log_widget.insert(tk.END, line)
            log_widget.see(tk.END)

    threading.Thread(target=run, daemon=True).start()


# ------------------------------------------------------------
#  INTERFACE
# ------------------------------------------------------------

root = tk.Tk()
root.title("Interface Essaim - Contrôle")

# Charger configuration existante
cfg = load_config()
full_json_data = cfg["full"]


# ----------------------- ZONE LOGS -------------------------

log = scrolledtext.ScrolledText(root, width=80, height=22)
log.pack(padx=10, pady=10)


# --------------------- CADRE PARAMÈTRES ---------------------

frame_params = ttk.LabelFrame(root, text="Paramètres")
frame_params.pack(fill="x", padx=10, pady=5)

# Mode
mode_var = tk.IntVar(value=cfg["mode"])
tk.Label(frame_params, text="Mode :").grid(row=0, column=0, padx=5, pady=5, sticky="w")

tk.Radiobutton(frame_params, text="Simulation", variable=mode_var, value=0)\
    .grid(row=0, column=1, sticky="w", padx=10)

tk.Radiobutton(frame_params, text="Réel", variable=mode_var, value=1)\
    .grid(row=0, column=2, sticky="w", padx=10)

# Nombre de drones
tk.Label(frame_params, text="Nombre de drones :").grid(row=1, column=0, padx=5, pady=5, sticky="w")

nb_drones_var = tk.StringVar(value=str(cfg["nb_drones"]))
tk.Entry(frame_params, textvariable=nb_drones_var, width=10)\
    .grid(row=1, column=1, sticky="w", padx=10)

# Bouton validation
def valider_parametres():
    """Valide les paramètres, met à jour le JSON et active les boutons ROS."""
    try:
        nb = int(nb_drones_var.get())
        if nb < 1:
            raise ValueError
    except ValueError:
        log.insert(tk.END, "[ERREUR] Le nombre de drones doit être un entier >= 1\n")
        log.see(tk.END)
        return

    # Sauvegarde JSON
    save_config(mode_var.get(), nb, full_json_data)

    log.insert(tk.END,
               f"\n✔ Paramètres validés :\n"
               f"  → Mode = {mode_var.get()}\n"
               f"  → nb_drones = {nb}\n\n")
    log.see(tk.END)

    # Désactiver réglages
    for w in widgets_params:
        w.config(state="disabled")

    # Activer boutons ROS
    for b in boutons_ros:
        b.config(state="normal")


btn_valider = tk.Button(frame_params, text="Valider", bg="#ccffcc",
                        command=valider_parametres)
btn_valider.grid(row=1, column=2, padx=10)


# Liste des widgets paramètre pour désactivation ultérieure
widgets_params = frame_params.winfo_children()


# ------------------------- BOUTONS ROS -----------------------

frame_actions = ttk.LabelFrame(root, text="Actions")
frame_actions.pack(fill="x", padx=10, pady=10)

def init_system():
    run_cmd_async("ros2 launch crazyflie_control launch.py", log)

def takeoff():
    run_cmd_async("ros2 launch crazyflie_control takeoff.launch.py", log)

def lancer_nodes():
    run_cmd_async("ros2 run tortues observer", log)
    run_cmd_async("ros2 launch fusion_CP_Consensus essaim_launch.yaml", log)

def land():
    nb = int(nb_drones_var.get())
    for i in range(1, nb + 1):
        run_cmd_async(f"ros2 service call /crazyflie_{i}/land std_srvs/srv/Trigger", log)

def kill_all():
    run_cmd_async("pkill -f ros2", log)


# Création boutons (désactivés par défaut)
boutons_ros = []

def add_button(text, callback, row, col, w=25, h=1, bg="white", fg="black", span=1):
    b = tk.Button(frame_actions, text=text, width=w, height=h,
                  command=callback, bg=bg, fg=fg, state="disabled")
    b.grid(row=row, column=col, padx=10, pady=5, rowspan=span)
    boutons_ros.append(b)


add_button("1. Initialisation", init_system, 0, 0)
add_button("2. Décollage", takeoff, 1, 0)
add_button("3. Action", lancer_nodes, 2, 0)
add_button("ATTERISSAGE", land, 0, 1, w=20, h=3, bg="lightgreen", span=3)
add_button("KILL", kill_all, 0, 2, w=20, h=3, bg="red", fg="white", span=3)

root.mainloop()
