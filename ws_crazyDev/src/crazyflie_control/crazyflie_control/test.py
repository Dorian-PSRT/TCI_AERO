#%%
import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie


def simple_takeoff():
    # Initialiser la Crazyradio
    cflib.crtp.init_drivers()
    available = cflib.crtp.scan_interfaces()
    link_uri = ""

    if not available:
        print(" 1 : Aucun Crazyflie détecté.")
        return

    for i in available:
        radio_name = i[0]
        print(f"1 : Interface trouvée : {radio_name} ({i[1]})")
        if "radio" in radio_name:
            link_uri = radio_name
            break

    if not link_uri:
        print("Aucune interface radio valide trouvée.")
        return

    print(f" Connexion au Crazyflie sur {link_uri}")

    # Connexion synchrone (plus simple et fiable)
    with SyncCrazyflie(link_uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf
        commander = cf.commander

        print(" Décollage...")
        for _ in range(50):  # environ 3 secondes de montée
            commander.send_velocity_world_setpoint(0.0, 0.0, 0.3, 0.0)
            time.sleep(0.01)
'''
        print(" Maintien position...")
        for _ in range(10):  # rester 2 secondes en l'air
            commander.send_velocity_world_setpoint(0.0, 0.0, 0.0, 0.0)
            time.sleep(0.01)

        print(" Maintien position...")
        for _ in range(200):  # rester 2 secondes en l'air
            commander.send_velocity_world_setpoint(0.0, 0.0, 0.0, 0.0)
            time.sleep(0.01)

        print("🛬 Atterrissage...")
        for _ in range(100):  # descente douce
            commander.send_velocity_world_setpoint(0.0, 0.0, -0.3, 0.0)
            time.sleep(0.01)

        commander.send_stop_setpoint()
        print("Fin du vol, drone posé.")
'''

# Lancer le script
if __name__ == '__main__':
    simple_takeoff()


#%%
'''
import sys
sys.path.append("../lib")
'''

import cflib.crtp
import time
from cflib.crazyflie import Crazyflie

# Initialize the low-level drivers (don't list the debug drivers)
cflib.crtp.init_drivers(enable_debug_driver=False)

print(" 2 : Scanning interfaces for Crazyflies...")

if True:
    # Create a Crazyflie object without specifying any cache dirs
    cf = Crazyflie()

    def handle_connected(link_uri):
        print("Connected to %s" % link_uri)

        print("Sending thrust 45000")
        cf.commander.send_setpoint(0, 0, 0, 45000)
        #time.sleep(0.75)
        print("Stopping thrust; hovering")
        cf.commander.send_setpoint(0, 0, 0, 32767)
        cf.param.set_value("flightmode.althold", "True")

    def close_link():
        print('Closing')
        cf.commander.send_setpoint(0, 0, 0, 0)
        time.sleep(0.1)
        cf.close_link()

    # Connect some callbacks from the Crazyflie API
    cf.connected.add_callback(handle_connected)

    link_uri = "radio://0/3/2M"
    print("Connecting to %s" % link_uri)

    # Try to connect to the Crazyflie
    cf.open_link(link_uri)

    # Variable used to keep main loop occupied until disconnect
    is_connected = True

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        close_link()
else:
    print("No Crazyflies found, cannot run example")


# %%
import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie


def simple_takeoff():
    #  Initialiser la Crazyradio
    cflib.crtp.init_drivers()
    available = cflib.crtp.scan_interfaces()
    link_uri = ""

    if not available:
        print("3: Aucun Crazyflie détecté.")
        return

    for i in available:
        radio_name = i[0]
        print(f"3 : Interface trouvée : {radio_name} ({i[1]})")
        if "radio" in radio_name:
            link_uri = radio_name
            break

    if not link_uri:
        print(" Aucune interface radio valide trouvée.")
        return

    print(f" Connexion au Crazyflie sur {link_uri}")

    # Connexion synchrone
    with SyncCrazyflie(link_uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf
        commander = cf.commander

        roll = 0.0
        pitch = 0.0
        yawrate = 0.0

        print(" Décollage (thrust progressif)...")

        thrust = 10001  # point de départ
        #commander.send_setpoint(roll, pitch, yawrate, thrust)
        print(" Maintien d'altitude approximatif...")
        for _ in range(30):  # maintien ~3s
            commander.send_setpoint(roll, pitch, yawrate, 20000)
            time.sleep(0.01)
'''
        for _ in range(30):  # montée douce (~3s)
            thrust += 400  # augmenter un peu chaque fois
            if thrust > 42000:
                thrust = 42000  # limite haute de sécurité
            commander.send_setpoint(roll, pitch, yawrate, thrust)
            time.sleep(0.01)

        print(" Maintien d'altitude approximatif...")
        for _ in range(30):  # maintien ~3s
            commander.send_setpoint(roll, pitch, yawrate, 40000)
            time.sleep(0.1)

        print("🛬 Atterrissage progressif...")
        for _ in range(30):  # descente douce
            thrust -= 800
            if thrust < 20000:
                thrust = 20000
            commander.send_setpoint(roll, pitch, yawrate, thrust)
            time.sleep(0.1)

        commander.send_setpoint(0, 0, 0, 0)
        commander.send_stop_setpoint()
        print(" Fin du vol, drone posé.")
'''

if __name__ == '__main__':
    simple_takeoff()


# %%