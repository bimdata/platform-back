Platform Backend
=================

BIMData Platform Backend is a the backend for the BIMData Platform application.


Technical view of the Platform
-------------------------------

The BIMData Platform Backend is written in Python 3.

Pre-requisites
---------------

You need:
 * a running Database System: we recommend PostGresQL, MariaDB
 * Python 3
 * PipEnv: [Download pipenv](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)

## Install

### Clone this repo
```
git clone https://github.com/bimdata/platform-back.git
```
### Launch the dedicated environment

 Place yourself in the proper directory: 
```
cd platform-back
pipenv shell
```
### Install all requirements with pipenv
```
pipenv install
```
##  Configure your environment
The .env file
The `bimdata/.env` file is a representation of additionnal ENV variable in order to override default config.
You can duplicate `.env.example` in `.env` and customize your config
```
cp .env.example .env
```
### Create a super-user

Create a super user (access to admin page)
```
./manage.py createsuperuser
```

## Database
* Create the database and edit the configuration file `.env`
* Create the tables and populate the database:

```
./manage.py migrate
```

## Launch your local instance

### Run the dev server
```
./manage.py runserver
```

## Testing

`./manage.py test` to run tests

### Troubleshooting

#### If `psycopg2` is missing (Ubuntu)

Install `libpq-server` with your packet manager, and re-do the procedure from the dependencies installation:

``` 
sudo apt install libpq-server
pipenv install
```

