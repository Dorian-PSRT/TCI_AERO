# Objectifs :

- [x] Update firmware CrazyRadio PA / Crazyflie 2.0  
- [x] Contrôler le drone avec une node sur ROS2  
- [x] Utiliser OptiTrack avec les Crazyflie
  
- [x] Récupérer les coordonées du drone sur PC Ubuntu
- [ ] Faire un PID pour les positions x,y,z du drone (règler le PID)
- [x] Calibrer l'optitrack (définir un centre (0,0,0))

# Liens utiles

[Lien GitHub Bitcraze](https://github.com/bitcraze)   
[How to Flash Firmware to Crazyflie 2.0 | Step-by-Step Guide for Beginners (vidéo 04:45)](https://www.youtube.com/watch?v=LGqCM9dPIPo)    
[Linux Xbox Controller Driver: A Comprehensive Guide](https://linuxvox.com/blog/linux-xbox-controller-driver/)   
[Github Amid Omidfar Crazyflie + ROS2 + OptiTrack](https://github.com/Amir-Omidfar/Crazyflie/tree/master)   
[Github Wolfgang Hönig Crazyflie + ROS](https://github.com/whoenig/crazyflie_ros)   
[Github Repository crazyflie-lib-python](https://github.com/bitcraze/crazyflie-lib-python/blob/master/docs/installation/install.md)     
[Lien GitHub Crazyflie + OptiTrack](https://github.com/juliordzcer/crazyflie_ros)       
[Tutorials Crazyswarm2/ROS2](https://imrclab.github.io/crazyswarm2/tutorials.html)    

# Client + cflib

## Liens utiles Bitcraze.io

[***Getting started with the Crazyflie 2.0 or Crazyflie 2.1(+)***](https://www.bitcraze.io/documentation/tutorials/getting-started-with-crazyflie-2-x/)   
[***Installation***](https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/installation/install/)   
[***USB permissions***](https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/installation/usb_permissions/)   
[***Userguide cfclient GUI***](https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/userguides/userguide_client/)    
[***The Crazyflie Python API explanation***](https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/python_api/)     
[***USB and Radio protocol of the Crazyradio dongle***](https://www.bitcraze.io/documentation/repository/crazyradio-firmware/master/functional-areas/usb_radio_protocol/)      
[***Recovery firmware flashing***](https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/userguides/recovery-mode/)        
[***Step-by-Step: Connecting, logging and parameters***](https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/sbs_connect_log_param/)     

[Troubleshooting](https://www.bitcraze.io/support/troubleshooting/)  
[Crazyradio firmware update](https://www.bitcraze.io/documentation/repository/crazyradio-firmware/master/building/programming/)   
[Build & Flash Instructions (crazyradio PA)](https://www.bitcraze.io/documentation/repository/crazyradio-firmware/master/building/building_flashing/)   
[Installing USB driver on Windows](https://www.bitcraze.io/documentation/repository/crazyradio-firmware/master/building/usbwindows/)    
[Crazyradio PA](https://www.bitcraze.io/products/crazyradio-pa/)   
[DFU update of the STM32F405](https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/development/dfu/)   
[UART communication](https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/development/uart_communication/)    
[Switching to Crazyflie-link-Cpp by default](https://www.bitcraze.io/2021/05/switching-to-crazyflie-link-cpp-by-default/)   

## Liens utiles forums

[Questions regarding using crazyflie client on Linux](https://forum.bitcraze.io/viewtopic.php?t=4660)   
[How to learn firmware version crazyflie?](https://forum.bitcraze.io/viewtopic.php?t=1884)    
[why doesn't flashing crazyflie(2.0) work in cfclient?](https://forum.bitcraze.io/viewtopic.php?p=22201#p22201)    
[Crazyflie Keyboard Control - A simple approach](https://forum.bitcraze.io/viewtopic.php?t=1182)    
[CrazyRadio not able to Connect to Scan for crazyflie](https://forum.bitcraze.io/viewtopic.php?t=1743)    
[Problems with Firmware Upgrade](https://forum.bitcraze.io/viewtopic.php?t=5075)    
[Solid or Blinking M2 LED [Solved]](https://forum.bitcraze.io/viewtopic.php?t=2185)  
[[SOLVED] Connection multiples crazyflies with cflib on ROS2](https://forum.bitcraze.io/viewtopic.php?p=23412)

# Crazyflie + nodes python   

## Liens utiles 

[The Crazyflie Python API explanation](https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/user-guides/python_api/)     
[Lien liste méthodes commander](https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/api/cflib/crazyflie/commander/)    
[Changer l'adresse du crazyflie](https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/userguides/userguide_client/#firmware-configuration)
[Lien bitcraze high level commander](https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/api/cflib/crazyflie/high_level_commander/)

## Notes

The Crazyflie Python API explanation :   

> - Code pour trouver l’URI du drone à commander
> - Cette page permet d’accéder au code python pour se connecter au drone et les commandes qui peuvent être utilisées
> - Exemple de paramètres de vol :
> ```
> roll = 0.0 # aller à gauche ou à droite 
> pitch = 0.0 # avancer ou reculer 
> yawrate = 0 # fait pivoter le drone à gauche ou à droite 
> thrust = 10001 # de 10001 à 60000(pleine puissance) 
> #self.crazyflie -> nom de l’objet Crazyflie() créé 
> self.crazyflie.commander.send_setpoint(roll, pitch, yawrate, thrust)
> ```

# Crazyswarm2

## Liens utiles 

[Documentation crazyswarm2](https://crazyswarm.readthedocs.io/en/latest/)  
[Lien installation Crazyswarm2](https://imrclab.github.io/crazyswarm2/installation.html#first-installation)   
[Lien GitHub crazyswarm2](https://github.com/IMRCLab/crazyswarm2?tab=readme-ov-file)    

[Crazyswarm2 development](https://www.bitcraze.io/2022/10/crazyswarm2-development/)   
[Lien info license GitHub](https://github.com/IMRCLab/crazyswarm2/blob/main/LICENSE)   
[Crazyswarm: a large nano-quadcopter swarm (Sep. 2016) (vidéo 01:49)](https://www.youtube.com/watch?v=D0CrjoYDt9w)   
[Crazyswarm: A powerful framework for aerial swarms - Wolfgang Hönig (vidéo 51:51)](https://www.youtube.com/watch?v=9KlfFpv6NIQ)   
[Crazyswarm: A Powerful Framework for Aerial Swarms in Research and Education](https://www.bitcraze.io/about/events/documents/bam2021/hoenig_crazyswarm_bam2021.pdf)  

## Notes

Crazyswarm est un ensemble de package pyhton  : il contient des nodes ROS2 pour piloter des drones.  

Lien installation Crazyswarm2 :  

> - créer un fichier .yaml pour initialiser les différentes configurations   
> - changer les adresses des drones dans le client  

Différences crazyswarm2 : 
- intégration mocap   
- marqueurs mocap indentiques ou seuls (libobjecttracker)
- broadcast
- simulation
- fondation ROS
- python firmware bindings

# OptiTrack 

## Liens utiles

[Quadcopter Optitrack Setup Tutorial (vidéo 15:35)](https://www.youtube.com/watch?v=5e0sMf48cBk)   
[How to use Motive Optitrack system (vidéo 15:00)](https://www.youtube.com/watch?v=Chs6PuK4QRM&t=120s)   
[crazyflie using optitrack (vidéo 0:20)](https://www.youtube.com/watch?v=LIUlkpsvITk)   
[Hovering Crazyflie Autonomously using ROS+Optitrack](https://uclalemur.com/blog/hovering-crazyflie-autonomously-using-ros-optitrack)   
[Lien GitHub motion_capture_tracking](https://github.com/IMRCLab/motion_capture_tracking/tree/ros2)   
