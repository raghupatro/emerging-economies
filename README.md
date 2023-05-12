# Emerging Economies Website

## basic setup

1. git clone the repo
2. create a venv `python -m venv venv`
3. activate the venv `venv\Source\Activate.ps1`
4. install the required dependencies `pip install -r requirements.txt`
5. cd into the project directory
6. `python manage.py runserver`

## working

+ emerging_economies is the project folder, contains all the Django apps
+ it contains the manage.py file, which is used to run all django commands
+ emerging_economies/emerging_economies is the "main" app folder, it contains settings.py, wsgi.py etc
+ emerging_economies/urls.py contains the url patterns, it can be then tied to individual apps
+ emerging_economies/emer_econ_app is our emerging economies app, which is shown on the page
+ contains various files whose explanation is given below

## Files in emer_econ_app

### migrations/ contains the database changes

### static/ contains our static files, images, style sheets, js, etc

### templates/ contains our html templates which are to be rendered by "views" (functions in views.py which handle individual pages)

### __init__.py tells that this directory is a python package

### admin.py ...no changes

### apps.py ...no changes

### models.py contains the Database models

### tests.py ... to write tests for any function

### urls.py maps the urls in this app to different views

### views.py contains all our views