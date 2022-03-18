# LTC++
## A modern, elegant and versatile course management system
### Database demo
Hello everyone! Here is how to populate some dummy data into the database for testing.

* First, make sure you have a proper virtual environment with Django==2.1.5
* Then, run the following commands to create a database.
  You may want to back up or delete your previous one.

```
python manage.py makemigrations ltc_main
python manage.py migrate
```

* Next, populate some dummy data and start the server.

```
python populate_ltc.py
python manage.py runserver
```

* Then, go to

```
http://127.0.0.1:8000/admin/
```

* To gain administrative access, please log in with the following information.

```
Username: 	admin
Password: 	123456
```
* You can try adding new courses inside the database to understand the 
  association between the data.
### Backend demo
* You can visit the index page now.
```
http://127.0.0.1:8000/ltc/
```
* Follow the links on that page to register and login.
* Here are some pre-registered student accounts:
```
Username:       Mikayla      Nur       Donald        Sue
Password: 	Mikayla123   Nur123    Donald123     Sue123
```
* Some staff accounts as well:
```
Username:       Radhika       Peyton
Password: 	Radhika123    Peyton123
```
* You can find these accounts in populate_ltc.py