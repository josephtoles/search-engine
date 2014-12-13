search engine
=============


Installation
------------

### Basic Setup (Mac)
1. Enter the project root folder
```
cd <project root>
```

2. Install [homebrew](http://mxcl.github.com/homebrew/)
```
ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)”
```

3. Install python
```
brew install python
```

3.5
```
pip install virtualenv
pip install virtualenvwrapper  # might not be necessary
source "/usr/local/bin/virtualenvwrapper.sh"
```

4. Create a virtual environment
```
mkvirtualenv search
```

5. Switch to that virtual environment
```
workon search
```

6. Install the requirements
```
pip install -r requirements.txt
```

7. Install postgres
```
git push --set-upstream origin postgres
```
Then run postgres with the command
```
postgres
```
You may need to add
```
export PGDATA="/usr/local/var/postgres"
```
to your ~/.bash_profile

8. Create your postgres database
To do this, run psql, then type the SQL command
    CREATE DATABASE postgres;
Then quit psql with \q
This database should really be called "search" and not "postgres". This is a bug.

9. Sync the database
```
./manage.py syncdb
```
If you choose not to create a superuser when prompted you can create one later with
```
./manage.py createsuperuser
```

10. Run the server
```
./manage.py runserver
```

You should get something like
```
System check identified 4 issues (0 silenced).
November 28, 2014 - 12:27:37
Django version 1.7.1, using settings 'search.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

11. Now open up a web browser and go to http://127.0.0.1:8000/. This should bring you to the search engine homepage.


Running Server
--------------

Three commands are necessary to run the server properly

To run the postgres database, call
```
postgres
```
This does not require you to be in your virtual environment.

To run the web interface run
```
./manage.py runserver
```
This requires you to be in your virtual environment.

To run the crawler, run
```
./manage.py auto_crawl
```
This requires you to be in your virtual environment.


Extra Commands
--------------

To run all unit tests
    ./manage.py test

To run flake8
    tox

To manually crawl a url
    ./manage.py crawl_url_subdomains <http://website.com/>

To create a superuser
    ./manage.py createsuperuser

To mess with the PostgreSQL database (Help is "\?")
    psql


Migrations
----------

Whenever you modify a model you will need to create a migration using
    ./manage.py makemigrations

Then everyone with a database will need to run manually
    ./manage.py migrate

Troubleshooting
---------------

If the database doesn't work, try running
```
./manage.py syncdb
```
This could be caused whenever anyone commits a change to the underlying models
