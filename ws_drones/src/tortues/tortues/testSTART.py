import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
#from turtlesim.srv import Spawn_Request

class TurtleSpawner(Node):
    def __init__(self):
        super().__init__('turtle_spawner')

        # Attente du service /spawn
        self.client = self.create_client(Spawn, '/spawn')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Le service /spawn n\'est pas encore disponible, j\'attends...')

        # Liste des positions où spawn les tortues
        self.spawn_positions = [
            (2.0, 2.0, 0.0),   # (x, y, theta) pour la première tortue
            (4.0, 4.0, 0.0),   # (x, y, theta) pour la deuxième tortue
            (6.0, 2.0, 0.0), # (x, y, theta) pour la troisième tortue
            (8.0, 5.0, 0.0), # (x, y, theta) pour la quatrième tortue
            # (1.0, 7.0, 0.0) # (x, y, theta) pour la cinquième tortue
        ]

        # Appel des services pour spawn les tortues
        self.spawn_turtles()

    def spawn_turtles(self):
        # Création de l'objet service request
        for i, pos in enumerate(self.spawn_positions, 1):
            x, y, theta = pos
            request = Spawn.Request()  # Utilisation de Spawn.Request() ici

            # Remplissage des champs de la requête
            request.x = x
            request.y = y
            request.theta = theta
            request.name = f'turtle{i}'

            # Appel du service /spawn
            self.get_logger().info(f"Spawning turtle {i} at position ({x}, {y}, {theta})")
            future = self.client.call_async(request)

            # Attente du résultat du service
            rclpy.spin_until_future_complete(self, future)
            if future.result() is not None:
                self.get_logger().info(f"Tortue {i} spawnée avec succès.")
            else:
                self.get_logger().error(f"Échec du spawn pour la tortue {i}.")

def main(args=None):
    rclpy.init(args=args)
    spawner = TurtleSpawner()
    rclpy.spin(spawner)
    spawner.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
