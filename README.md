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
Username:       Amelia      Emily       Jack        Mason
Password: 	Amelia123   Emily123    Jack123     Mason123
```
* Some professor accounts as well:
```
Username:       Charlotte       Harry
Password: 	Charlotte123    Harry123
```
* You can find these accounts in populate_ltc.py

# Changelog
All notable changes to this project will be documented in this file.
## [1.0.0] - 2022-02-14
### Added
* Initial commit.
## [1.0.1] - 2022-02-15
### Added
* README file added.
### Changed
* Models.py updated.
## [1.0.2] - 2022-02-16
### Added
* Index, login and registration page added.
* Human-readable changelog added.
* Users can add courses now.
* Users can add assignments now.
* Log out function added.
* Student page added.
* Professor page added.
* Course page added.
### Fixed
* Typo:   Assigment -> Assignment
## [1.0.3] - 2022-02-18
### Added
* requirements.txt added.
* Users can add timeslots now.
* Assignment page added.
* Timeslot page added.
* More dummy data.
### Changed
* Rename: TimePeriod -> TimeSlot
