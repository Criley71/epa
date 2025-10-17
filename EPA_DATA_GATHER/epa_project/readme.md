# EPA Project
## 1. Get an API key 
just enter this with your email into an address bar. They will send you an email with your api key

`https://aqs.epa.gov/data/api/signup?email=myemail@example.com `

## 2. Set up python virtual environment
*I am assuming that you are using a linux environment*

make a venv folder

`python3 -m venv venv`

activate the venv

`source venv/bin/activate`

install dependencies

`pip install -r requirements.txt`

## 3. Setup Postgresql

Install:

  `sudo apt install postgresql postgresql-contrib`

Open Postgres:

`psql -U postgres`

Make a new database: 

```
CREATE DATABASE epa_data; 
CREATE USER epa_user WITH PASSWORD 'yourpassword';
ALTER ROLE epa_user SET client_encoding TO 'utf8';
ALTER ROLE epa_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE epa_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE epa_data TO epa_user;
```

## 4. Setting up the django server
make a .env file in the django root (same folder as where the manage.py is) and in the .env fill out these variables:
```
DATABASE_URL=postgres://<username>:<password>@localhost:5432/<dbname>
EPA_API_EMAIL=<your_epa_api_email>
EPA_API_KEY=<your_epa_api_key>
```

in one terminal run

`python manage.py runserver`

in another do:

```
python manage.py makemigrations
python manage.py migrate 
python manage.py createsuperuser
python manage.py get_epa_data
```

the server should be running on local host 8000 so go to http://127.0.0.1:8000/admin and sign in using the info you used for createsuperuser 

