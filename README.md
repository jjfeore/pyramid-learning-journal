# Learning Journal Assignment

Creating our own Learning Journal with the Pyramid framework, and using Jinja2 for templating. 

**Authors**:

- James Feore (jjfeore@gmail.com)
- Morgan Nomura

## Progress:

*May 29, 2017*
Completed HTML/CSS mockups for the learning journal pages.

*May 30, 2017*
Added routes/views, completed tests, and deployed to Heroku at https://learning-journal-jjfeore.herokuapp.com/

## Routes:

- `/` - the home page and a listing of all journal entries
- `/journal/{id:\d+}` - see a detailed view of an existing entry
- `/journal/{id:\d+}/edit-entry` - edit an existing journal entry
- `/journal/new-entry` - add a new entry to the database

## Set Up and Installation:

- Clone this repository to your local machine.

- Once downloaded, `cd` into the `pyramid-learning-journal` directory.

- Begin a new virtual environment with Python 3 and activate it.

- `cd` into the next `learning_journal` directory. It should be at the same level of `setup.py`

- `pip install` this package as well as the `testing` set of extras into your virtual environment.

- `$ initialize_db development.ini` to initialize the database, populating with random models.

- `$ pserve development.ini --reload` to serve the application on `http://localhost:6543`

## To Test

- If you have the `testing` extras installed, testing is simple. If you're in the same directory as `setup.py` type the following:

```
$ tox
```