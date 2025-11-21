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
            commander.send_velocity_world_setpoint(0.0, 0.0, 0.5, 0.0)
            time.sleep(0.1)
        
        print(" atterit")
        for _ in range(30):  # environ 3 secondes de montée
            commander.send_velocity_world_setpoint(0.0, 0.0, -0.3, 0.0)
            time.sleep(0.1)
            
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