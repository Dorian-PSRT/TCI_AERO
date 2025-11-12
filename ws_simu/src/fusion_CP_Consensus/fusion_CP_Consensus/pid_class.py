# import time
# class PID():
#     def __init__(self, kp = 1, ki = 0, kd = 0):
#         self.kp = kp
#         self.ki = ki
#         self.kd = kd
#         self.ierr = 0
#         self.last_err = 0
#         self.last_t = 0

#     def run(self, err):
#         self.ierr = self.ierr  + err
#         #derr = (er - self.last_err) / self.dt
#         u = self.kp * err + self.ki * self.ierr #+ self.kd * derr 

#         return u

class PID():
    def __init__(self, kp=1, ki=0, kd=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.ierr = 0
        self.last_err = None

    def run(self, err, dt=0.1):
        self.ierr += err * dt
        self.ierr = max(-5, min(5, self.ierr))  # anti-windup

        if self.last_err is None:
            derr = 0
        else:
            derr = (err - self.last_err) / dt

        u = self.kp * err + self.ki * self.ierr + self.kd * derr
        self.last_err = err
        return u
