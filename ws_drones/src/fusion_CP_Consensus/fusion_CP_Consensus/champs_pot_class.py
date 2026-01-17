#version modifiée par ChatGPT pour isoler Z du champ X,Y en 2D
import numpy as np
from geometry_msgs.msg import Point

class CP():
    def __init__(self, coeff_attraction = 2, coeff_repu = 9, coeff_prev = 0.2,
                 rayon_obstacle = 1.5, rayon_secu = 0.15,
                 coeff_pas = 0.2, taille_du_pas_min=0.1, taille_du_pas_max = 0.5):

        #stockage des paramètres dans des variables globales:
        self.Kattr     = coeff_attraction
        self.Krepu     = coeff_repu
        self.Kprev     = coeff_prev
        self.d_0       = rayon_obstacle
        self.r_s       = rayon_secu
        self.Kpas_err  = coeff_pas
        self.Kpas_min  = taille_du_pas_min   
        self.Kpas_max  = taille_du_pas_max        
        self.Kpas_old  = 0.1

        # ---- PARAMÈTRES VERTICAUX SÉPARÉS ----
        self.Kz        = 0.1         # gain vertical (augmente si tu veux monter plus vite)
        self.VZ_MAX    = 1.0         # m/s max (sécurité)
    

    #=========  Champ potentiel 2D inchangé  =========#

    def norme_erreur(self, goal, pose):
        err = np.array([goal.point.x, goal.point.y]) - np.array([pose.x, pose.y])
        return np.linalg.norm(err), err

    def force_attr(self, goal, pose, k):
        return k * self.norme_erreur(goal,pose)[1]

    def force_repu(self, obstacles, pose_robot, k, d_0, sigma=2, max_force=2):
        f_repu = np.array([0.0, 0.0])
        pose = np.array([pose_robot.x, pose_robot.y])
        err_l = [1000]

        for obs in obstacles:
            obsV = np.array([obs.x, obs.y])
            err  = pose - obsV
            err_l.append(np.linalg.norm(err))

            d   = np.linalg.norm(err) - self.r_s
            d_0 = obs.z  # rayon obstacle

            if d <= 0:
                grad_d = err / np.linalg.norm(err)
                f_repu += k * np.exp(-d**2 / (2 * sigma**2)) * grad_d

            elif d < d_0:
                grad_d = err / np.linalg.norm(err)
                f_repu += (k / d**2) * np.exp(-d**2 / (2 * sigma**2)) * grad_d
                f_repu = np.clip(f_repu, -max_force, max_force)

        self.err_min_obs = min(err_l)
        return f_repu
    

    def set_next_step(self, goal, pose, obstacles):

        #-----------  XY  (champ potentiel 2D)  ----------------#
        err_pose = self.norme_erreur(goal,pose)[0]

        if abs(err_pose) > 0.1:
            f_attr  = self.force_attr(goal, pose, self.Kattr)
            f_repu  = self.force_repu(obstacles, pose, self.Krepu, self.d_0)
            f_walls = self.force_frontieres(pose, self.Krepu)

            F = f_attr + f_repu + f_walls

        else:
            F = np.array([0.0, 0.0])

        # ----- Pas XY ----- #
        if np.linalg.norm(F) > 0:
            Kpas = np.clip(self.err_min_obs*self.Kpas_err, self.Kpas_min, self.Kpas_max) #On calcul un Kpas borné dépendant de la distance avec l'obstacle le plus proche : "Plus le drone est proche d'un obstacle, plus le pas est petit"
            diff = Kpas - self.Kpas_old

            if abs(diff) >= (self.Kpas_max - self.Kpas_min):
                Kpas = self.Kpas_old + np.sign(diff)*(self.Kpas_max - self.Kpas_min)

            next_xy = Kpas * F / np.linalg.norm(F)
            self.Kpas_old = Kpas
        else:
            next_xy = np.array([0.0, 0.0])
            Kpas = self.Kpas_min

        #-----------  Z  INDÉPENDANT  ----------------#
        dz = self.Kz * (goal.point.z - pose.theta)
        dz = np.clip(dz, -self.VZ_MAX, self.VZ_MAX)

        #-----------  Résultat final 3D (XY + Z indépendant)  ----------#
        nextStep = np.array([next_xy[0], next_xy[1], dz])

        # période identique à avant (ne dépend pas du Z)
        period = -0.6*Kpas**2 + 0.8*Kpas + 0.25    #On calcul une période de rafraichissement pour avoir un comportement plus fluide en simulation
                # Cette période est calculée en fonction de trois points de fonctionnement éfficaces (Kpas,période)
        return nextStep, period #0.5


    # === Fonctions annexes inchangées === #
    def force_frontieres(self, pose, k, sigma=2):
        f_walls = np.array([0.0, 0.0])
        if pose.x >= 2.5:
            d = abs(3 - pose.x)
            f_walls += (k/d**2)*np.exp(-d**2/(2*sigma**2))*np.array([1.0,0])
        if pose.x <= -2.5:
            d = abs(-3 + pose.x)
            f_walls += (k/d**2)*np.exp(-d**2/(2*sigma**2))*np.array([-1,0])
        if pose.y >= 4.5:
            d = abs(5 - pose.y)
            f_walls += (k/d**2)*np.exp(-d**2/(2*sigma**2))*np.array([0,1])
        if pose.y <= -4.5:
            d = abs(-5 + pose.y)
            f_walls += (k/d**2)*np.exp(-d**2/(2*sigma**2))*np.array([0,-1])
        return f_walls

