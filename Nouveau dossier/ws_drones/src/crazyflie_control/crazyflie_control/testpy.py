#%%
from threading import Thread
import motioncapture

host_name = '192.168.2.10'
import time
# The type of the mocap system
# Valid options are: 'vicon', 'optitrack', 'optitrack_closed_source', 'qualisys', 'nokov', 'vrpn', 'motionanalysis'
mocap_system_type = 'optitrack'

# The name of the rigid body that represents the Crazyflie
# mettre de nom de l'objet rigid qui est dans optitrack
rigid_body_name = 'crazyflie_1'


class MocapWrapper(Thread):
    #_instance = None
    #_lock = threading.Lock()

    #def __new__(cls, *args, **kwargs):
    #    # Double-checked locking pour éviter les conditions de course
    #    if cls._instance is None:
    #        with cls._lock:
    #            if cls._instance is None:
    #                cls._instance = super(MocapWrapper, cls).__new__(cls)
    #    return cls._instance

    def __init__(self):
        # Empêche l'exécution multiple du constructeur
        #   if getattr(self, "_initialized", False):
        #       return
        super().__init__()
        
        self.body_name = {}
        self.host_name = host_name
        self.on_pose = None
        self._stay_open = True

        self._initialized = True
        self.start()

    def close(self):
        self._stay_open = False

    def run(self):
        mc = motioncapture.connect(mocap_system_type, {"hostname": host_name})
        
        while self._stay_open:
            mc.waitForNextFrame()
            for name, obj in mc.rigidBodies.items():
                print(name)
                

            #pos = obj.position
                    

#%%

#%%

if __name__ == "__main__":
    m = MocapWrapper()


