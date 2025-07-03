deactivate
sudo apt-get update
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential python3-venv pkg-config libmysqlclient-dev -y

git reset --hard
sudo git clean -fxd
git pull
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
sudo .env/bin/python3 manage.py runserver 0.0.0.0:7000