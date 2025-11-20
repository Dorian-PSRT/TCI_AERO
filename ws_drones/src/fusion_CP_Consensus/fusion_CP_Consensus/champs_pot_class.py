import numpy as np
#import des types
from geometry_msgs.msg import Point


class CP():
    def __init__(self, coef_attraction = 2, coef_repu = 3, coeff_prev = 2, rayon_obstacle = 1.5, taille_du_pas = 1.5):
        self.Kattr = coef_attraction
        self.Krepu = coef_repu
        self.Kprev = coeff_prev
        self.d_0   = rayon_obstacle
        self.Kpas  = taille_du_pas
        

    def norme_erreur(self, goal, pose):
        err = np.array([goal.point.x, goal.point.y]) - np.array([pose.x, pose.y])
        err_pose = np.linalg.norm(err)
        return err_pose,err

    def force_attr(self, goal, pose, k):
        
        f_attr = k * self.norme_erreur(goal,pose)[1]
        return f_attr

    def force_repu(self, obstacles, pose_robot, k, d_0, sigma=2, max_force=3):
        f_repu = np.array([0.0, 0.0])
        pose = np.array([pose_robot.x, pose_robot.y])
        for obs in obstacles:
            obsV=np.array([obs.x, obs.y])  #En effet, obs est du type Point (Cf fake_ot_node et local_path_node)
            #print(f"obsV____________:({obsV}")
            err = pose - obsV  
            d   = np.linalg.norm(err) - 1.0 #correspond à la distance entre l'obstacle et la zone de sécurité du drone de rayon 1
            d_0 = obs.z

            if d <= 0:                     #cas où la zone de sécurité du drone touche l'obstacle
                grad_d = err / np.linalg.norm(err)
                #f_repu += k*(1/d_0)**2*(1/d-1/d_0)*grad_d   #asymptotique
                f_repu += k * np.exp(-d**2 / (2 * sigma**2)) * grad_d   #gaussienne
                
            elif d < d_0:                   #cas où le drone arrive dans le rayon de l'obstacle
                grad_d = err / np.linalg.norm(err)
                #f_repu += (k/d**2)*(1/d-1/d_0)*grad_d   #asymptotique
                f_repu += (k / d**2) * np.exp(-d**2 / (2 * sigma**2)) * grad_d   #gaussienne
                f_repu=np.clip(f_repu, -max_force, max_force)

            else:                           #cas où le drone est hors du rayon de l'obstacle
                f_repu += np.array([0.0, 0.0])

        return f_repu
    

    def set_next_step(self, goal, pose, obstacles):
        err_pose = self.norme_erreur(goal,pose)[0]

        if abs(err_pose) > 0.1:
            f_attr      = self.force_attr(goal, pose, self.Kattr) #appel de la fonction force_attr
            f_repu      = self.force_repu(obstacles, pose, self.Krepu, self.d_0)    #si on n'est pas encore arrivé on appel force_repu
            angle       = self.angle_vect(f_attr,f_repu)
            vect        = self.vect_prev(f_attr)    #calcul un vecteur unitaire orthogonal à f_attr
            if angle >= 85:
                f_prevision = angle*self.Kprev*vect
            else:
                f_prevision = 0*vect

            F = f_attr + f_repu + f_prevision                                                        #le vecteur qui défini le prochain pas correspond à la sommes des vecteurs de forces atractives et répulsives
                        
        nextStep = self.Kpas * F/np.linalg.norm(F)
        return nextStep
    
    def force_frontieres(self, pose):
        if (pose.x <=1):
            f_walls += 2
        if (pose.x >=9):
            f_walls += 2
        if (pose.y <=1):
            f_walls += 2
        if (pose.y >=9):
            f_walls += 2

        f_walls = 3
        return f_walls
    
    def angle_vect(self,A,B): #np array

        dot_product = np.dot(A, B)

        magnitude_A = np.linalg.norm(A)
        magnitude_B = np.linalg.norm(B)

        angle_radians = np.arccos(dot_product / (magnitude_A * magnitude_B))

        angle_degrees = np.degrees(angle_radians)
        return angle_degrees
    
    def vect_prev(self,A):
        if A[0] == 0: #cas particulier où x=0
            return np.array([1.0,0.0])
        else:
            y = np.sqrt(1/((A[0]/A[1])**2+1))
            x = -A[0]/A[1]*y
            return np.array([x,y])