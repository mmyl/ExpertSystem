# Expert System for IT security risk analysis

# TODO
- Pyke integration
- Admin role and view
<!-- - Link without login -->
<!-- - Mandatory fields for input -->
<!-- - Link to Edit page -->
<!-- - Choose category -->
<!-- - Gather answers -->
<!-- - Questionaire page -->
<!-- - Report page -->

 <!-- login page -->

## Prerequisites
- Visual Studio Code for code editing
- Download Git
- Install Flask (under virtual env)
	- pip install Flask
- Installation of Python 3.10.1
- Create Github repository

### Create virtual environment with specific python version
virtualenv --python='C:\Users\AdminUser\AppData\Local\Programs\Python\Python38\python.exe' virenv
.\virenv\Scripts\activate
 pip install -r requirements.txt

 *deactivate* to deactive virtual env

 set FLASK_ENV=development

### Create database
> python
> from app import db
> db.create_all()
> exit()

<!-- list tables name -->
db.engine.table_names()

<!-- Insert New Category -->
>>> from app import Categories
>>> from app import db
>>> update = Categories(category='Kopijos', description='Saugumo klausimai susiję su atsarginių kopijų sauga.')
>>> db.session.add(update)
>>> db.session.commit()

update = Categories(category='BDAR', description='Saugumo klausimai susiję su Bendruoju Duomenų Apsaugos Reglamentu.')
update = Categories(category='Slaptažodžiai', description='Saugumo klausimai susiję su slaptažodžių sauga.')

## Development
Set environment variables 
 $env:FLASK_APP="app"
 $env:FLASK_ENV="development"

# Questions
Does Every Employee Have a Strong Password?
Are Your Employees Required to Change Their Passwords Regularly?
When Possible, Do You Use Two-Factor Authentication?
Do Your Employees Use Their Personal Smartphones for Work Purposes?
Are You Backing Up Your Files?
Does Every Company Device Have Antivirus and Malware Software Installed?
Have You Limited the Amount of Employees with Admin Access to Only Those Who Absolutely Need it?
Are Your Employees Trained in Recognizing Phishing Emails?
Do Your Employees Know Never to Give Sensitive Information to Supervisors Via Email?
Do You Encrypt Databases and Customer Information?
Do you have (x) security certification?
Do you have (x) security measure in place?
Do you have any physical data protection measures in place?
Have you had any breaches or security issues in the past?
Do you have a disaster recovery or business continuity plan?
Do you have cyber security or liability insurance?


# Reference
https://www.youtube.com/watch?v=Z1RJmh_OqeA

https://flask.palletsprojects.com/en/2.0.x/

http://pyke.sourceforge.net/logic_programming/index.html

Phishing
![image](https://user-images.githubusercontent.com/80095026/160441105-e2632e69-e64b-48c4-9841-014b46acb3ba.png)
![image](https://user-images.githubusercontent.com/80095026/160442547-3b1cf7c8-7253-4565-9366-5497ee770b42.png)
![image](https://user-images.githubusercontent.com/80095026/160441412-597da583-079d-49ff-b526-670416b57a52.png)


