
<h1 align="center">skychallange</h1>
<p align="center">My solution proposals for skygate's junior python develeper recruitment tasks.</p>

# Chapter I

## Installation

Chapter I solution is located in directory of the same name. 
It requires [Python](https://www.python.org/) 3.5+ to run.

Install the dependencies, apply migrations, optionally install fixtures and start the server.

```sh
$ cd .\ChapterI\
$ pip install -r requirements.txt
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py loaddata data.json # All passwords for users are 'password'
$ python3 manage.py runserver
```

## Running with docker

```sh
$ cd .\ChapterI\
$ docker build -t skychallange .
$ docker run -p 8000:8000 -i -t skychallange
```

## Running the tests

```sh
$ python3 manage.py test
```

## API Endpoints

`/auth/login/` - (POST) Returns Token key  
`/auth/logout/` - (POST) Logouts  
`/exams/` - (POST | GET) Lists all exams  
`/exams/id/` - (ALL) Details about an exam  
`/exams/id/archivize/` - (POST | PATCH | PUT) Archivizes or dearchivizes an exam  
`/tasks/` - (POST | GET) Lists all tasks  
`/tasks/id/` - (ALL) Logouts

# Chapter II

## Installation

Chapter II solution is located in directory of the same name. 
It requires [Python](https://www.python.org/) 3.5+ to run.

Solutions for chapter II don't require third party libraries.

```sh
$ cd .\ChapterII\
$ python3 .\solution1.py
How many skyphrases are valid?
Answer: 383
$ python3 .\solution2.py
What is the sum of all numbers in the document?
Answer: 111754
```
