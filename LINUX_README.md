=============
search engine
Linux setup
=============

A note to the reader:
These instructions were originally developed for Bodhi,
a stripped-down Ubuntu-based Linux. Your system may behave
a bit differently. Please solve problems creatively.

------------

Installation

1. Make sure you have Python 2.7 installed

1.5: Note: "sudo" may not be strictly necessary for the python installation. Using it is your choice.

1.75. Install Python dev. This is required for some pip packages
$ sudo aptitude install python-dev

2. Install pip
$ sudo aptitude install python-pip

3. Install virtualenv
$ sudo pip install virtualenv

4. Install virtualenvwrapper
$ sudo pip install virtualenvwrapper

5. Add the following line to your ~/.bashrc file
source /usr/local/bin/virtualenvwrapper.sh

6. Restart bash
$ bash
or close the shell and reopen it

7. Create a virtualenv. You can cal it whatever you want. For the purposes of these
instructions, we will call it "search". While you are workin in your virtual
environment, your command prompt will be prefixed with "(search)" as in

(search)joseph@yui:~/code/search-engine$

To create a virtual environment, use the following command:

$ mkvirtualenv search

To workon on an existing virtual environment, use the following command:

$ workon search

You should now be workin in your virtual environment. In case you want to delete them, virtualenvs are stored in ~/.virtualenvs.

8. Install the requirements
pip install -r requirements.txt
This may throw an error. If it does, try installing all the requirements except that that threw an error.
Self: ignore psycopg2


[note to self: ignored some pg_config errors here]

9. Install PostgreSQL
$ sudo apt install postgresql
Correction. Install dev version
# sudo apt install postgresql-dev-all

10. Create a user for postgres
$ sudo -u postgres createuser <your username>

11. Create a database for postgres
$ psql -d template1

11.5
Here is where things get tricky. Unlike in Mac, Linux postgres has its own users and roles that are seperate from your OS. Generally there is a dedicated superuser, postgres. To log in as postgres, use the command
$ sudo -i -u postgres
And to logout from postgres type Ctrl+d

Now, when you are acting as the postgres user, you can create databases with the command
$ createdb <database-name>
So create a database called search
$ createdb search

11.6
To enter modify the database manually with SQL, enter
$ psql -d search
You can then enter SQL directly. There are a couple special commands to help you out
$ \l  # list tables
$ \d  # list databases
$ \q  # exit postgres

12. Checkpoint. Postgres should now have three databases
postgres
template0
template1

You can check this by typing
$ psql postgres
# \l
# \q

13. Check that the server works
$ ./manage.py runserver






