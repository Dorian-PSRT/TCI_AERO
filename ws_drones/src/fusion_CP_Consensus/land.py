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





