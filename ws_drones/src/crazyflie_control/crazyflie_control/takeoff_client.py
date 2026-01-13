import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger  # ou le type exact du service Takeoff de Crazyflie

class TakeoffClient(Node):
    def __init__(self, namespace):
        super().__init__('takeoff_client_' + namespace)
        self.cli = self.create_client(Trigger, f'/{namespace}/takeoff')
        self.cli_init = self.create_client(Trigger, f'/{namespace}/init_param')

        while not self.cli_init.wait_for_service(timeout_sec=0.5):
            self.get_logger().info(f'Service /{namespace}/init_param not available, waiting...')
        
        self.call_init_param()

        while not self.cli.wait_for_service(timeout_sec=0.5):
            self.get_logger().info(f'Service /{namespace}/takeoff not available, waiting...')
        
        self.call_takeoff()

    def call_takeoff(self):
        req = Trigger.Request()
        future = self.cli.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info(f'{self.cli.srv_name} success!')
        else:
            self.get_logger().error(f'{self.cli.srv_name} failed')

    def call_init_param(self):
        req = Trigger.Request()
        future = self.cli_init.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info(f'{self.cli_init.srv_name} success!')
        else:
            self.get_logger().error(f'{self.cli_init.srv_name} failed')

def main(args=None):
    rclpy.init(args=args)
    import sys
    namespace = sys.argv[1] if len(sys.argv) > 1 else "crazyflie_1"
    node = TakeoffClient(namespace)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
