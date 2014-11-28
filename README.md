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
pip install requirements.txt
```

7. Sync the database
```
./manage.py syncdb
```

8. Run the server
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

9. Now open up a web browser and go to http://127.0.0.1:8000/. This should bring you to the search engine homepage.


Running Server
--------------

This is a search engine.


To manually creawl a url, use the command
    ./manage.py crawl_url_subdomains http://website.com/
Or similar


To run this code you need to run two commands
    ./manage.py runserver  # runs the server
    ./manage.py auto_crawl # runs the crawler

