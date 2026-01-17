import subprocess
from time import sleep


for i in range(1,5):
    #os.system(f"ros2 service call /crazyflie_{i}/land std_srvs/srv/Trigger")
    subprocess.Popen(
    ["ros2", "service", "call", f"/crazyflie_{i}/land", "std_srvs/srv/Trigger"]
    )

sleep(5)

terminal_type="gnome-terminal"
subprocess.run(["pkill", "-f", terminal_type], check=False)












# from pathlib import Path

# # Dossiers
# dossier = Path(__file__).parent #dossier du script
# workspace_path = dossier.parents[1]

# titre_terminal = "TEMP_ne_pas_fermer"
# terminal_type="gnome-terminal"

# def open_terminal(*cmd):
#     full_cmd = (
#         f"source {workspace_path}/install/setup.bash; "  #f"source ~/Desktop/TCI_AERO/ws_drones/install/setup.bash; " 
#         + " ".join(cmd)
#         + "; exec bash"
#     )

#     subprocess.Popen([
#         terminal_type,
#         "--title", titre_terminal,
#         "--",
#         "bash", "-c", full_cmd
#     ])


##########################""