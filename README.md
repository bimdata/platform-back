Platform Backend
=================

BIMData Platform Backend is a the backend for the BIMData Platform application.


Technical view of the Platform
-------------------------------

The BIMData Platform Backend is written in Python 3.

Pre-requisites
---------------

You need:
 * Python 3.6 or later
 * PipEnv: [Download pipenv](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)
 * a running database system: we support PostgreSQL only. 

    **Note:** Any other DBMS compatible with Django should work, but we don't officially support them

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

## Documentation

Check https://developers.bimdata.io.
Our documentation helps you to understand the concepts and architecture of the Platform. 


Need more [information about the API](https://developers.bimdata.io/api/index.html)?

Need some details [about the authentication workflow](https://developers.bimdata.io/guide/authentication_bimdata_connect.html)?

## Testing

`./manage.py test` to run tests

### Troubleshooting

#### If `psycopg2` is missing (Ubuntu)

Install `libpq-server` with your packet manager, and re-do the procedure from the dependencies installation:

``` 
sudo apt install libpq-server
pipenv install
```

