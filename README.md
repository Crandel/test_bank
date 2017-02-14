## __A simple bank management system__

# **Install Instruction** #


First of all you need python 3.6 and node.js/npm installed

Please install all necessary dependencies

```bash
sudo npm install -g webpack
pip install -r requirements.txt
npm install
webpack
```

When it will be done you must add config env file there will be your secure settings( database connection, secret salt etc.) from example *env.example*

```bash
cp env.example .env
```

When you can change all needed env variables(set passwords for example)

```bash
nano .env
```

At last you could run the server

```bash
$ python manage.py collectstatic --noinput

$ python manage.py migrate

$ python manage.py runserver
```

Your website will be available on localhost address or any host you set in .env
