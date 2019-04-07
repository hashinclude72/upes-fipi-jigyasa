# UPES FIPI JIGYASA
<img src="https://www.fipi.org.in/employees_data/images/fipi.png" height="70">&nbsp;&nbsp;<img src="https://github.com/jaswal72/upes-fipi-jigyasa/blob/master/static/images/jigyasa.png" height="80">  


This is a website made to host JIGYASA annual event by UPES FIPI student chapter. It is hosted in heroku. This website contains user authentication system (login/logout) and paytm payments gateway.  
[JIGYASA](https://www.upesjigyasa.com/)  
[Heroku link](https://upesjigyasa.herokuapp.com/)  

This repo is a fully functional website suitable for an academic project, small business or similar.  
* Python 3.6  
* Django 2.1.7  
* PostgreSQL (recommended), MySQL, Oracle Database and SQLite  

## Set up the website
* Clone the repo  
`https://github.com/jaswal72/upes-fipi-jigyasa.git`

* Open Project directory  
* Now install the requirements  
`pip install -r requirements.txt`

* Set Environment variables
* Make Migrations  
`python manage.py makemigrations`

* Migrate paytm app for transactions details  
`python manage.py migrate`

* Create Super user  
`python manage.py createsuperuser`

* Now in terminal run the server and go to http://localhost:8000/  
`python manange.py runserver`
<br>

#### You should now be able to see your homepage!!!  
#### Change the pages as you wish.

## Acknowledgments

The front end is based on the HTML, Bootstrap.  
The back end is based on django.

#### For any issues contact me at:
shubham__jaswal@hotmail.com
