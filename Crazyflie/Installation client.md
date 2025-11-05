**Ubuntu/Linux**  

En premier lieu, dans le cmd, taper les lignes suivantes :  
```
sudo apt install git python3-pip libxcb-xinerama0 libxcb-cursor0
pip3 install --upgrade pip
```
Ensuite, set up udev permissions :  

Tout d'abord,
```
sudo groupadd plugdev
sudo usermod -a -G plugdev $USER
```
Log out and log in again. 
Copier-coller le bloc suivant :  
```
cat <<EOF | sudo tee /etc/udev/rules.d/99-bitcraze.rules > /dev/null
# Crazyradio (normal operation)
SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="7777", MODE="0664", GROUP="plugdev"
# Bootloader
SUBSYSTEM=="usb", ATTRS{idVendor}=="1915", ATTRS{idProduct}=="0101", MODE="0664", GROUP="plugdev"
# Crazyflie (over USB)
SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5740", MODE="0664", GROUP="plugdev"
EOF
```
Cela fera apparaître le fichier 99-bitcraze.rules dans le dossier /etc/udev/rules.d  
Taper ensuite ces 2 lignes :  
```
sudo udevadm control --reload-rules
sudo udevadm trigger
```
On va ensuite installer librairies et client, mais avant cela, il est conseillé de créer un virtual environment (venv) afin de les y installer.   
Pour ce faire : 
```
python3 -m venv ~/.virtualenvs
```
A savoir que la librairie et le client ne sont supportés que sur Python3, donc toujours utiliser python3 et pip3.   
Pour activer le venv :
```
source ~/.virtualenvs/bin/activate
```
Dans celui-ci, installer crazyflie library (cflib) : 
```
pip3 install cflib
```
Puis installer le client :
```
pip3 install cfclient
```
Pour accéder au client, il suffit de taper la ligne suivante lorsque l'on se trouve dans le venv :
```
cfclient
```

**Annexe**

Pour voir quels périphériques sont connectés en USB :
```
lsusb
```
Pour vérifier la version du firmware du crazyradio PA dongle :
```
lsusb -d 1915:7777 -v | grep bcdDevice
```
