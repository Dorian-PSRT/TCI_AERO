
class PID():
    def __init__(self, kp = 1, ki = 0, kd = 0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.ierr = 0
        self.last_err = 0
        self.last_t = 0

    def run(self, err):
        self.ierr = self.ierr  + err
        #derr = (er - self.last_err) / self.dt
        u = self.kp * err + self.ki * self.ierr #+ self.kd * derr 

        return u
