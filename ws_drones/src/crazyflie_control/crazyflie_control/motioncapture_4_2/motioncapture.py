import socket, time
from threading import Event, Thread
from crazyflie_control.motioncapture_4_2.NatNetClient import NatNetClient

def receive_rigid_body( rb_id, pos, rot):
    #self.rigid_body[rb_id] = {'pos': pos, 'rot': rot}    
    print( rb_id, pos, rot)
    
class MotionCaptureNatNet(Thread):
    def __init__(self, hostname):
        Thread.__init__(self)
        self.server_ip = hostname
        self._rb = {}              # id → {name, pos, rot}
        self._stay_open = True
        self.local_ip = self._detect_local_ip(hostname)
        self.callback_rigid_body = None
        self.client = NatNetClient()
        self.client.set_client_address(self.local_ip)
        self.client.set_server_address(hostname)
        self.client.set_use_multicast(True)
        self.rigid_body = {}
        self.client.rigid_body_listener = receive_rigid_body
        self.client.run("d")
        print("start")

    # ---------------------------------------------------------
    def _detect_local_ip(self, remote_ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect((remote_ip, 1511))
            return s.getsockname()[0]
        finally:
            s.close()

    # ---------------------------------------------------------
    def close(self):
        self._stay_open = False
        try:
            self.client.shutdown()
        except:
            pass

    def run(self):
        while self._stay_open:
            for id, value in self.rigid_body.items():
                if not self.callback_rigid_body:        
                    self.callback_rigid_body(id, value['pos'],value['rot'])
                time.sleep(0.1)

    

        


if __name__ == "__main__":
    mc = MotionCaptureNatNet(hostname="192.168.2.10")
    mc.start()