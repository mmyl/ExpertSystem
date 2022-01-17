# Expert System for IT security risk analysis

# TODO
- Update doesn't return full question
- login page
- Questionaire page
- Report page
- Pyke integration?

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

### Create database
> python
> from app import db
> db.create_all()
> exit()


## Development
Set environment variables 
 $env:FLASK_APP="hello"
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


Are Your Websites Properly Protected?


# Reference
https://www.youtube.com/watch?v=Z1RJmh_OqeA


