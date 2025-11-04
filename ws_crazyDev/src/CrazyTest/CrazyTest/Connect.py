import rclpy
import time
from rclpy.node import Node 
import cflib.crtp
from cflib.crazyflie import Crazyflie
from rclpy.executors import MultiThreadedExecutor


class SimpleNode2(Node):
    def __init__(self):
        super().__init__('node2')  # Nom du nœud

        # Initialiser les CrazyRadio pour trouver le drone
        cflib.crtp.init_drivers()
        #available = cflib.crtp.scan_interfaces()
        #for i in available:
            #print("Interface with URI [%s] found and name/comment [%s]" % (i[0], i[1]))
        self.crazyflie = Crazyflie() #création d'un objet python représentant le drone
        #évènement : quand la connection au drone est établie
        self.crazyflie.connected.add_callback(self.crazyflie_connected)
        self.crazyflie.open_link("radio://0/80/2M") #initie la connexion au drone


    #appelé lorsque la connexion au drone est établie
    def crazyflie_connected(self, uri):
        print("Connecté au drone :", uri)
        # envois des commandes une fois la connexion établie
        self.send_setpoint()

    def send_setpoint(self):
        #Initialise les commandes de vol
        roll    = 0.0   # aller à gauche ou à droite
        pitch   = 0.0   # avancer ou reculer
        yawrate = 0     # fait pivoter le drone à gauche ou à droite
        thrust  = 10001 # de 10001 à 60000 (pleine puissance)
        self.get_logger().info('Envoie les commandes de vols')
        self.crazyflie.commander.send_setpoint(roll, pitch, yawrate, thrust)
        time.sleep(2) #le drone continue d'exécuter la commande précédente pendant ce temps
        self.send_stop()

    def send_stop(self):
        roll    = 0.0   # aller à gauche ou à droite
        pitch   = 0.0   # avancer ou reculer
        yawrate = 0.0   # fait pivoter le drone à gauche ou à droite
        thrust  = 0 # de 10001 à 60000(pleine puissance)
        self.get_logger().info('Stop')
        self.crazyflie.commander.send_setpoint(roll, pitch, yawrate, thrust)


def main(args=None):
    rclpy.init(args=args)
    executor = MultiThreadedExecutor()
    node = SimpleNode2()  # Création du nœud
    executor.add_node(node)
    #rclpy.spin(node)  # Exécution du nœud
    executor.spin()
    
    node.destroy_node()  # Destruction du nœud lors de l'arrêt
    rclpy.shutdown()  # Arrêt de ROS2

if __name__ == '__main__':
    main()