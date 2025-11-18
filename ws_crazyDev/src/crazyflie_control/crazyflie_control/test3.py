import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie


def simple_takeoff():

    #  Initialiser la Crazyradio
    cflib.crtp.init_drivers()
    available = cflib.crtp.scan_interfaces()
    link_uri = ""
    '''
    if not available:
        print("3: Aucun Crazyflie détecté.")
        return



    for i in available:
        radio_name = i[0]
        print(f"3 : Interface trouvée : {radio_name} ({i[1]})")
        if "radio" in radio_name:
            link_uri = radio_name
            break
    '''
    link_uri = "radio://0/82/2M/E7E7E7E7E7"
    print("Connecting to %s" % link_uri)

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
