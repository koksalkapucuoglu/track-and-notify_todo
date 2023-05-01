# track-and-notify_todo
This project is a todo management app. The user can describe own todo status, todo and 
notify herself todo's in the desired status in certain periods. Here is a solution for this application using django, 
celery, celery-beat and rabbitmq in the backend.

## Tech Stack

**Core Tech:** Python

**Backend Service:** Django, Django Rest Framework

**Authentication:** Basic Token, JWT Token

**Database:** Postgresql

**API Documentation:** Swagger

**Task Management and Broker**: Celery, Celery-Beat RabbitMQ, Redis

**Task Monitoring**: Flower

## Run Locally using Docker

Clone the project

```bash
  git clone https://github.com/koksalkapucuoglu/track-and-notify_todo.git
```

Go to the project directory

```bash
  cd track-and-notifiy_todo
```

Build

```bash
  docker-compose build
```

Create local_settings.py and fill required fields

```bash
  mv local_settings.py.dev local_settings.py
```

Setup database tables by running migrations

```bash
  docker-compose run --rm app python manage.py makemigrations
  docker-compose run --rm app python manage.py migrate
```

Run project

```bash
  docker-compose up
```

## Run Locally using environment

Clone the project

```bash
  git clone https://github.com/koksalkapucuoglu/track-and-notify_todo.git
```

Go to the project directory

```bash
  cd track-and-notify_todo
```

Create python env

```bash
  python -m venv env
```

Activate enviroment

```bash
  source env/Scripts/activate
```

or

```bash
  env\Scripts\activate
```

Install requirements

```bash
  pip install -r requirements.txt
```

Create local_settings.py and fill required fields

```bash
  mv local_settings.py.dev local_settings.py
```

Detect and apply django model changes

```bash
  python manage.py makemigrations
  python manage.py migrate
```

Create superuser to login Django admin panel

```bash
  python manage.py createsuperuser
```

Run django project

```bash
  python manage.py runserver
```

## Project Screenshots

Notify Entries

```json
  [
  {
    "id": 35,
    "status": {
      "id": 15,
      "code": "INPROGRESS",
      "name": "In Progress",
      "order": 2,
      "user": 35
    },
    "user": {
      "id": 35,
      "username": "screenshot",
      "email": "roheri8556@saeoil.com"
    },
    "minute": "36",
    "hour": "*",
    "day_of_month": "*",
    "month_of_year": "*",
    "day_of_week": "*",
    "title": "Get my in_progress tasks at 36 minutes of every hour"
  },
  {
    "id": 34,
    "status": {
      "id": 14,
      "code": "TODO",
      "name": "To Do",
      "order": 1,
      "user": 35
    },
    "user": {
      "id": 35,
      "username": "screenshot",
      "email": "roheri8556@saeoil.com"
    },
    "minute": "*/1",
    "hour": "*",
    "day_of_month": "*",
    "month_of_year": "*",
    "day_of_week": "*",
    "title": "Get my todo tasks each 1 minute"
  }
]
```

Task Monitoring

![Task Monitoring](https://github.com/koksalkapucuoglu/track-and-notify_todo/blob/master/ss/flower.png?raw=true)

Email Content

![Task Monitoring](https://github.com/koksalkapucuoglu/track-and-notify_todo/blob/master/ss/email.png?raw=true)

## Version Backlog
**v0.4**
- Added project build documentation
- 
**v0.3**
- Added reminders to users about their tasks via email

**v0.2**
- Added todo status management
- Added todo management
- Added token-based user authentication

**v0.1**
- Added login and registration, forgot password, change password functionality for users
- Added basic and jwt token-based user authentication for improved security
- Added swagger documentation