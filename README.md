# Installation

**Python v3.8 is required to run this application**

## TL;DR

Clone the repository:

```bash
$ git clone https://git@github.com/nomad-back.git
``` 

Install required python packages in a new virtual environment:

```bash
$ cd nomad-back
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

Process with deployment:

```bash
$ cd nomad
$ export DJANGO_SETTINGS_MODULE="nomad.settings.dev"
$ python manage.py migrate
$ python manage.py compilemessages
$ python manage.py createsuperuser
Adresse email: super@user.com
Prénom: super
Nom de famille: user
Password: 
Password (again): 
Superuser created successfully. 
```

Start the server:

```bash
$ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
August 08, 2022 - 20:25:42
Django version 3.2.13, using settings 'nomad.settings.dev'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Start a browser to connect on the different endpoints:

  * `http://localhost:8000/admin/` to access the Django admin. Connect with the super-user previously created.
  * `http://localhost:8000/api/swagger/` or `http://localhost:8000/api/redoc/` to connect on the online API documentation.

