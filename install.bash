#!/bin/bash

echo "This is a work in progress"

sudo apt-get install python3
sudo pip3 install python3-xlib
sudo pip3 install pyautogui
sudo apt-get install vim -y

sudo cp /etc/rc.local /etc/rc.local-backup
sed '/exit 0/d' /etc/rc.local | sudo tee /etc/rc.local
sudo bash -c 'echo "cd `pwd`; python3 main.py" >> /etc/rc.local'
sudo bash -c 'echo "exit 0" >> /etc/rc.local'

echo "#!/bin/bash" > ~/Desktop/run
echo "cd `pwd`; python3 main.py" >> ~/Desktop/run
sudo chmod +x ~/Desktop/run
