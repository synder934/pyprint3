## requirements

raspberry pi
python 3.13

cd ~
wget https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tgz

sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev

tar -xzvf Python-3.13.0.tgz
cd Python-3.13.0/
ls
./configure

sudo make altinstall
/usr/local/bin/python3.13 -V
sudo rm /usr/bin/python
sudo ln -s /usr/local/bin/python3.13 /usr/bin/python
python -VV

from https://wiki.lupsha.com/how-to-upgrade-to-python-3-12-on-raspberry-pi/
