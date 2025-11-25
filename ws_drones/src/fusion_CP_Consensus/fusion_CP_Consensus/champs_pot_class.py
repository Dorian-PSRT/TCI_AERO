import numpy as np
#import des types
from geometry_msgs.msg import Point


class CP():
    def __init__(self, coeff_attraction = 2, coeff_repu = 3, coeff_prev = 0.2, rayon_obstacle = 1.5, rayon_secu = 0.15, coeff_pas = 0.2, taille_du_pas_min=0.1, taille_du_pas_max = 0.5):
        self.Kattr     = coeff_attraction
        self.Krepu     = coeff_repu
        self.Kprev     = coeff_prev
        self.d_0       = rayon_obstacle
        self.r_s       = rayon_secu
        self.Kpas_err  = coeff_pas
        self.Kpas_min  = taille_du_pas_min   
        self.Kpas_max  = taille_du_pas_max        
        #init
        self.Kpas_old  = 0.1

    def norme_erreur(self, goal, pose):
        err = np.array([goal.point.x, goal.point.y]) - np.array([pose.x, pose.y])
        err_pose = np.linalg.norm(err)
        return err_pose,err

    def force_attr(self, goal, pose, k):
        
        f_attr = k * self.norme_erreur(goal,pose)[1]
        return f_attr

    def force_repu(self, obstacles, pose_robot, k, d_0, sigma=2, max_force=2):
        f_repu = np.array([0.0, 0.0])
        pose = np.array([pose_robot.x, pose_robot.y])
        err_l = [1000]
        for obs in obstacles:
            obsV=np.array([obs.x, obs.y])  #En effet, obs est du type Point (Cf fake_ot_node et local_path_node)

            err = pose - obsV  
            err_l.append(np.linalg.norm(err))
            d   = np.linalg.norm(err) - self.r_s #correspond à la distance entre l'obstacle et la zone de sécurité du drone de rayon r_s
            d_0 = obs.z   #obs.z est le rayon de l'obstacle

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

        self.err_min_obs=min(err_l)
        return f_repu
    


    def set_next_step(self, goal, pose, obstacles):
        err_pose = self.norme_erreur(goal,pose)[0]

        if abs(err_pose) > 0.1:
            f_attr      = self.force_attr(goal, pose, self.Kattr) #appel de la fonction force_attr
            f_repu      = self.force_repu(obstacles, pose, self.Krepu, self.d_0)    #si on n'est pas encore arrivé on appel force_repu
            f_walls     = self.force_frontieres(pose,self.Krepu)
            angle       = self.angle_vect(f_attr,f_repu)
            vect        = self.vect_prev(f_attr)    #calcul un vecteur unitaire orthogonal à f_attr
            if     angle >= 180:   # l'obstacle total est face à nous
                f_prevision = angle*self.Kprev*vect   #on se décale vers la gauche ou la droite
            elif   angle >= 85:    # l'obstacle total est devant nous
                f_prevision = np.array([0.0,0.0])
            else:                  # l'obstacle est derrière nous
                f_prevision = np.array([0.0,0.0])
                f_repu = np.array([0.0,0.0])
                self.err_min_obs = 1000.0

            F = f_attr + f_repu + f_prevision + f_walls                                                        #le vecteur qui défini le prochain pas correspond à la sommes des vecteurs de forces atractives et répulsives
        #,err_pose
        Kpas = np.clip(min([self.err_min_obs])*self.Kpas_err ,self.Kpas_min,self.Kpas_max)  #borné par Kpas_max et Kpas_min
        diff = Kpas-self.Kpas_old
        if abs(diff) >= (self.Kpas_max-self.Kpas_min): #Si il y un changement de pas trop brusque, alors on sature la variation
            Kpas=self.Kpas_old+np.sign(diff)*(self.Kpas_max-self.Kpas_min)
        nextStep = Kpas * F/np.linalg.norm(F)
        #period = -0.4*Kpas+0.7 #droite qui passe par les 2 points de fonctionnement (pas=0,5;0,5s) et (pas=1,5;0,1s) 
        period = -0.6*Kpas**2+0.8*Kpas+0.25 #courbe qui passe par les 3 points de fonctionnement (pas=0,5;0,5s), (pas=1,0;0,45s) et (pas=1,5;0,1s)   
        #period = 0.5*Kpas+0.05
        self.Kpas_old = Kpas
        return nextStep, period
    
    def force_frontieres(self, pose, k , sigma=2):
        f_walls = np.array([0.0,0.0])
        if (pose.point.x >=2.5):
            d = abs(3 - pose.point.x)
            f_walls += (k / d**2) * np.exp(-d**2 / (2 * sigma**2)) * np.array([1.0,0.0])
        if (pose.point.x <=-2.5):
            d = abs(-3 - pose.point.x)
            f_walls += (k / d**2) * np.exp(-d**2 / (2 * sigma**2)) * np.array([-1.0,0.0])
        if (pose.point.y >=4.5):
            d = abs(5 - pose.point.y)
            f_walls += (k / d**2) * np.exp(-d**2 / (2 * sigma**2)) * np.array([0.0,1.0])
        if (pose.point.y <=-4.5):
            d = abs(-5 - pose.point.y)
            f_walls += (k / d**2) * np.exp(-d**2 / (2 * sigma**2)) * np.array([0.0,-1.0])
        return f_walls
    
    def angle_vect(self,A,B): #np array

        dot_product = np.dot(A, B)

        magnitude_A = np.linalg.norm(A)
        magnitude_B = np.linalg.norm(B)

        if magnitude_A == 0 or magnitude_B == 0:
            angle_radians = 3.14
        else:
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