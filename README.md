Platform-back
==========

Install
---------
* Download pipenv: https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv
* `git clone git@github.com:bimdata/platform-back.git` : retrieve the repo
* `cd platform-back`
* `pipenv shell`
* `pipenv install` : install all requirements

Usage
------
* `./manage.py migrate` to create the database
* `./manage.py createsuperuser` to create a super user (access to admin page)
* `./manage.py runserver` to run a dev server
* `./manage.py test` to run tests


## The .env file
The `bimdata/.env` file is a representation of additionnal ENV variable in order to override default config.
You can duplicate `.env.example` in `.env` and customize your config
