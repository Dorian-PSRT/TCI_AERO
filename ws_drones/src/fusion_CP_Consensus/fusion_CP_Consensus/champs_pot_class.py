import numpy as np
#import des types
from geometry_msgs.msg import Point


class CP():
    def __init__(self, coef_attraction = 10, coef_repu = 10, rayon_obstacle = 3, taille_du_pas = 2):
        self.Kattr = coef_attraction
        self.Krepu = coef_repu
        self.d_0 = rayon_obstacle
        self.Kpas = taille_du_pas

    def norme_erreur(self, goal, pose):
        err = np.array([goal.point.x, goal.point.y]) - np.array([pose.x, pose.y])
        err_pose = np.linalg.norm(err)
        return err_pose,err

    def force_attr(self, goal, pose, k=10):
        
        f_attr = k * self.norme_erreur(goal,pose)[1]
        return f_attr

    def force_repu(self, obstacles, pose_robot, k = 10.0, d_0 = 2.0):
        f_repu = np.array([0.0, 0.0])
        pose = np.array([pose_robot.x, pose_robot.y])
        for obs in obstacles:
            obsV=np.array([obs.x, obs.y])  #En effet, obs est du type Point (Cf fake_ot_node et local_path_node)
            #print(f"obsV____________:({obsV}")
            err = pose - obsV  
            d = np.linalg.norm(err) - 1.0 #correspond à la distance entre l'obstacle et la zone de sécurité du drone de rayon 1

            if d <= 0:                     #cas où la zone de sécurité du drone touche l'obstacle
                grad_d = err / np.linalg.norm(err)
                f_repu += k*(1/d_0)**2*(1/d-1/d_0)*grad_d
                
            elif d < d_0:                   #cas où le drone arrive dans le rayon de l'obstacle
                grad_d = err / np.linalg.norm(err)
                f_repu += (k/d**2)*(1/d-1/d_0)*grad_d
                
            else:                           #cas où le drone est hors du rayon de l'obstacle
                f_repu += np.array([0.0, 0.0])

        return f_repu
    

    def set_next_step(self, goal, pose, obstacles):

        err_pose = self.norme_erreur(goal,pose)[0]
        f_attr = self.force_attr(goal, pose, k=self.Kattr) #appel de la fonction force_attr
        
        if abs(err_pose) > 0.1:
            f_repu = self.force_repu(obstacles, pose, k =0.7, d_0 = 15.0)    #si on n'est pas encore arrivé on appel force_repu
            F = f_attr + f_repu                                                         #le vecteur qui défini le prochain pas correspond à la sommes des vecteurs de forces atractives et répulsives
                        
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