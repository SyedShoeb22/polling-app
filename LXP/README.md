Version 1.0
# NubeEra
![developer](https://img.shields.io/badge/Developed%20By%20%3A-Imran%20Khan-red)
---
## Steps to Deploy
### Commands on Server:
```
deactivate                                                  # Deactivate .env   
cp db.sqlite3 /home/ubuntu                                  # copy database before losing it  
git reset --hard                                            # reset hard    
git clean -fxd                                              # clean and fix 
virtualenv .env                                             # create virtualenv called .env 
source .env/bin/activate                                    # Activate Environement 
pip install -r requirements.txt                             # Install all Dependencies 
python manage.py makemigrations                             # List Changes in database 
python manage.py migrate                                    # Apply Migration 
sudo .env/bin/python3 manage.py runserver 0.0.0.0:80        # run server on everywhere
```
### Admin
- Create Admin account using command
```
py manage.py createsuperuser
```
- After Login, can see Total Number Of Learner, Trainer, Course, Questions are there in system on Dashboard.
- Can View, Update, Delete, Approve Trainer.
- Can View, Update, Delete Learner.
- Can Also See Learner Marks.
- Can Add, View, Delete Course/Exams.
- Can Add Questions To Respective Courses With Options, Correct Answer, And Marks.
- Can View And Delete Questions Too.

### Trainer
- Apply for job in System. Then Login (Approval required by system admin, Then only trainer can login).
- After Login, can see Total Number Of Learner, Course, Questions are there in system on Dashboard.
- Can Add, View, Delete Course/Exams.
- Can Add Questions To Respective Courses With Options, Correct Answer, And Marks.
- Can View And Delete Questions Too.
> **_NOTE:_**  Basically Admin Will Hire Trainers To Manage Courses and Questions.

### Learner
- Create account (No Approval Required By Admin, Can Login After Signup)
- After Login, Can See How Many Courses/Exam And Questions Are There In System On Dashboard.
- Can Give Exam Any Time, There Is No Limit On Number Of Attempt.
- Can View Marks Of Each Attempt Of Each Exam.
- Question Pattern Is MCQ With 4 Options And 1 Correct Answer.
---

## HOW TO RUN THIS PROJECT
- Install Python(3.7.6) (Dont Forget to Tick Add to Path while installing Python)
- Open Terminal and Execute Following Commands :
```
python -m pip install -r requirements. txt
```
- Download This Project Zip Folder and Extract it
- Move to project folder in Terminal. Then run following Commands :
```
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```
- Now enter following URL in Your Browser Installed On Your Pc
```
http://127.0.0.1:8000/
```

## CHANGES REQUIRED FOR CONTACT US PAGE
- In settins.py file, You have to give your email and password
```
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'your email password'
EMAIL_RECEIVING_USER = 'youremail@gmail.com'
```

## Drawbacks/LoopHoles
- Admin/Trainer can add any number of questions to any course, But while adding course, admin provide question number.

## Docker File
- Here i created a docker file and its name is **myimage_setting** so instead of using Dockerfile name use **myimage_setting** to build docker image
