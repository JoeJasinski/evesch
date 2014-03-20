THIS PROJECT IS IN A STATE OF FLUX AS IT IS BEING UPGRATED TO SUPPORT DJANGO 1.6


This project is aimed at allowing organizations to create and manage events of different category types. 

## Requires:
- Django 1.6.2
- Python 2.6+
- Pillow
tested on OSX 10.9.2 

## Installation

### clone the repo
git clone https://github.com/JoeJasinski/evesch.git


### Browse to the project directory
cd ./evesch_8.1/evesch/

### sync the database tables
./manage.py syncdb
./manage.py migrate 

### say 'no' when it asks you to create a superuser

### init the test data
./manage.py jjj_init

## run the development server
./manage.py runserver

# browse to http://localhost:8000/  or http://localhost:8000/admin/

