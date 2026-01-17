


class PID ():
    def __init__(self,P,I,D):
        self.kP=P
        self.kI=I
        self.kD=D
        self.lastError=0
        self.totalError=0
    
    def calcul(self,error):
        
        self.totalError+=error

        p = self.kP*error
        i = self.kI*self.totalError
        d = self.kD*(error-self.lastError)

        if(error<=0.001):
            i=0

        self.lastError=error

        return p+i+d