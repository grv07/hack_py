# hack_py

How to scrap msg:
![Alt text](/../screen/screen/scrap.png?raw=true "Optional Title")


Home page:
![Alt text](/../screen/screen/home.png?raw=true "Optional Title")

Comments page:
![Alt text](/../screen/screen/comment.png?raw=true "Optional Title")

Add comment page:
![Alt text](/../screen/screen/add_comment.png?raw=true "Optional Title")

Nested Comment page:
![Alt text](/../screen/screen/nested_comment.png?raw=true "Optional Title")

login/register page:
![Alt text](/../screen/screen/login_register.png?raw=true "Optional Title")

Post news page:
![Alt text](/../screen/screen/post_news.png?raw=true "Optional Title")



Steps to setup postgres

1.sudo apt-get update

2.sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib

3.sudo -u postgres psql

4.CREATE DATABASE hnews;

5.CREATE USER root WITH PASSWORD 'root';

6.GRANT ALL PRIVILEGES ON DATABASE hnews TO root;

#Now create a virtual env and rn all migrations file.
