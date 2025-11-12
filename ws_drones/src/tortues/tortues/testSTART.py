import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
#from turtlesim.srv import Spawn_Request
from turtlesim.srv import Kill


class TurtleSpawner(Node):
    def __init__(self):
        super().__init__('turtle_spawner')

        # Attente du service /kill et /spawn
        self.kill_client = self.create_client(Kill, '/kill')
        self.spawn_client = self.create_client(Spawn, '/spawn')

        for client, name in [(self.kill_client, '/kill'), (self.spawn_client, '/spawn')]:
            while not client.wait_for_service(timeout_sec=1.0):
                self.get_logger().info(f"Le service {name} n'est pas encore disponible, j'attends...")

        # Supprime la tortue par défaut
        self.kill_default_turtle()

        # Liste des positions à spawn
        self.spawn_positions = [
            (2.0, 1.0, 0.0),
            (2.0, 3.0, 0.0),
            (2.0, 5.0, 0.0),
            (2.0, 7.0, 0.0),
        ]

        # Spawn des nouvelles tortues
        self.spawn_turtles()

    def kill_default_turtle(self):
        request = Kill.Request()
        request.name = 'turtle1'
        future = self.kill_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        self.get_logger().info('Tortue par défaut supprimée.')

    def spawn_turtles(self):
        for i, pos in enumerate(self.spawn_positions, 1):
            x, y, theta = pos
            request = Spawn.Request()
            request.x = x
            request.y = y
            request.theta = theta
            request.name = f'turtle{i}'
            self.get_logger().info(f"Spawning turtle{i} at ({x}, {y})")
            future = self.spawn_client.call_async(request)
            rclpy.spin_until_future_complete(self, future)
            if future.result():
                self.get_logger().info(f"Tortue {i} spawnée avec succès.")


def main(args=None):
    rclpy.init(args=args)
    spawner = TurtleSpawner()
    rclpy.spin(spawner)
    spawner.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()








# class TurtleSpawner(Node):
#     def __init__(self):
#         super().__init__('turtle_spawner')

#         #     Attente du service /kill et /spawn
#         self.kill_client = self.create_client(Kill, '/kill')
#         self.spawn_client = self.create_client(Spawn, '/spawn')

#         for client, name in [(self.kill_client, '/kill'), (self.spawn_client, '/spawn')]:
#             while not client.wait_for_service(timeout_sec=1.0):
#                 self.get_logger().info(f"Le service {name} n'est pas encore disponible, j'attends...")

#         # Supprime la tortue par défaut
#         self.kill_default_turtle()

#         # Liste des positions où spawn les tortues
#         self.spawn_positions = [
#             (2.0, 1.0, 50.0),   # (x, y, theta) pour la première tortue
#             (2.0, 3.0, 0.0),   # (x, y, theta) pour la deuxième tortue
#             (2.0, 5.0, 0.0), # (x, y, theta) pour la troisième tortue
#             (2.0, 7.0, 0.0), # (x, y, theta) pour la quatrième tortue
#             # (1.0, 7.0, 0.0) # (x, y, theta) pour la cinquième tortue
#         ]

#         # Appel des services pour spawn les tortues
#         self.spawn_turtles()

#     def kill_default_turtle(self):
#         request = Kill.Request()
#         request.name = 'turtle1'
#         future = self.kill_client.call_async(request)
#         rclpy.spin_until_future_complete(self, future)
#         self.get_logger().info('Tortue par défaut supprimée.')

#     def spawn_turtles(self):
#         # Création de l'objet service request
#         for i, pos in enumerate(self.spawn_positions, 1):
#             x, y, theta = pos
#             request = Spawn.Request()  # Utilisation de Spawn.Request() ici

#             # Remplissage des champs de la requête
#             request.x = x
#             request.y = y
#             request.theta = theta
#             request.name = f'turtle{i}'

#             # Appel du service /spawn
#             self.get_logger().info(f"Spawning turtle {i} at position ({x}, {y}, {theta})")
#             future = self.client.call_async(request)

#             # Attente du résultat du service
#             rclpy.spin_until_future_complete(self, future)
#             if future.result() is not None:
#                 self.get_logger().info(f"Tortue {i} spawnée avec succès.")
#             else:
#                 self.get_logger().error(f"Échec du spawn pour la tortue {i}.")
