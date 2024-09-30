[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/uwidcit/flaskmvc)
<a href="https://render.com/deploy?repo=https://github.com/uwidcit/flaskmvc">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>

![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Flask MVC Template
A template for flask applications structured in the Model View Controller pattern [Demo](https://dcit-flaskmvc.herokuapp.com/). [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)


# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing Dependencies
```bash
$ pip install -r requirements.txt
```

# Configuration Management


Configuration information such as the database url/port, credentials, API keys etc are to be supplied to the application. However, it is bad practice to stage production information in publicly visible repositories.
Instead, all config is provided by a config file or via [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/).

## In Development

When running the project in a development environment (such as gitpod) the app is configured via default_config.py file in the App folder. By default, the config for development uses a sqlite database.

default_config.py
```python
SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
```

These values would be imported and added to the app in load_config() function in config.py

config.py
```python
# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...
```

## In Production

When deploying your application to production/staging you must pass
in configuration information via environment tab of your render project's dashboard.

![perms](./images/fig1.png)

# Flask Commands

The database is initialized with mock data. Before executing the commands for the project requirements, initialize the database by executing the following command:

```bash
$ flask init
```


# Mock Data

## Staff Members

### Lecturers
| Title  | First Name | Last Name    | Role      |
|--------|------------|--------------|-----------|
| Dr.    | Jane       | Villanueva   | Lecturer  |
| Prof.  | Jackson    | Duke         | Lecturer  |
| Dr.    | Emily      | Cooper       | Lecturer  |
| Prof.  | Tony       | Stark        | Lecturer  |
| Dr.    | Camille    | Wilson       | Lecturer  |

### Tutors
| Title  | First Name | Last Name    | Role      |
|--------|------------|--------------|-----------|
| Mr.    | Robert     | Pattinson    | Tutor     |
| Ms.    | Lindsay    | Lohan        | Tutor     |
| Mr.    | James      | Charles      | Tutor     |
| Ms.    | Steven     | Harrison     | Tutor     |
| Mr.    | Kevin      | Hart         | Tutor     |

### Teaching Assistants (TAs)
| Title  | First Name | Last Name    | Role      |
|--------|------------|--------------|-----------|
| Mr.    | Mark       | Taylor       | TA        |
| Ms.    | Rachel     | Adams        | TA        |
| Mr.    | Michael    | Jordan       | TA        |
| Ms.    | Jessica    | Alba         | TA        |
| Mr.    | Daniel     | Radcliffe    | TA        |

## Courses

| Course Code | Course Name                       | Lecturer               | Tutor                | Teaching Assistant     |
|-------------|-----------------------------------|------------------------|----------------------|------------------------|
| COMP101     | Introduction to Computer Science  | Dr. Jane Villanueva     | Mr. Robert Pattinson  | Mr. Mark Taylor         |
| MATH102     | Discrete Maths                    | Prof. Jackson Duke      | Ms. Lindsay Lohan     | Ms. Rachel Adams        |
| ELEC201     | Electronics                       | Dr. Emily Cooper        | Mr. James Charles     | Mr. Michael Jordan      |
| ENG101      | Thermodynamics                    | Prof. Tony Stark        | Ms. Steven Harrison   | Ms. Jessica Alba        |
| COMP102     | Computer Programming              | Dr. Camille Wilson      | Mr. Kevin Hart        | Mr. Daniel Radcliffe    |



After initalizing the database, the following commands can be executed to demonstrate the project requirements:

Requirement #1 - creating a course:

```python
# inside wsgi.py

course_cli = AppGroup('course', help='Course object commands')

@course_cli.command("create", help="Creates a course")
@click.argument("course_code")
@click.argument("course_name")
@click.argument("lecturer_id")
@click.argument("tutor_id")
@click.argument("ta_id")
def create_course_command(course_code, course_name, lecturer_id, tutor_id, ta_id):
    course = create_course(course_code, course_name, lecturer_id, tutor_id, ta_id)

    # Fetch and display staff names
    lecturer = Staff.query.get(lecturer_id)
    tutor = Staff.query.get(tutor_id)
    ta = Staff.query.get(ta_id)

    lecturer_name = f"{lecturer.title} {lecturer.firstName} {lecturer.lastName}" if lecturer else "None"
    tutor_name = f"{tutor.title} {tutor.firstName} {tutor.lastName}" if tutor else "None"
    ta_name = f"{ta.title} {ta.firstName} {ta.lastName}" if ta else "None"

    print(f'Course {course.courseCode} created with:')
    print(f'Lecturer: {lecturer_name}')
    print(f'Tutor: {tutor_name}')
    print(f'Teaching Assistant: {ta_name}')



```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash
$ flask course create "course code" "course name" lecturer id tutor id TA id
```

For example: 

```bash
$ flask course create "COMP200" "Advanced Programming" 1 2 3
```

# Running the Project

_For development run the serve command (what you execute):_
```bash
$ flask run
```

_For production using gunicorn (what the production server executes):_
```bash
$ gunicorn wsgi:app
```

# Deploying
You can deploy your version of this app to render by clicking on the "Deploy to Render" link above.

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. This must also be executed once when running the app on heroku by opening the heroku console, executing bash and running the command in the dyno.

```bash
$ flask init
```

# Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```

# Testing

## Unit & Integration
Unit and Integration tests are created in the App/test. You can then create commands to run them. Look at the unit test command in wsgi.py for example

```python
@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))
```

You can then execute all user tests as follows

```bash
$ flask test user
```

You can also supply "unit" or "int" at the end of the comand to execute only unit or integration tests.

You can run all application tests with the following command

```bash
$ pytest
```

## Test Coverage

You can generate a report on your test coverage via the following command

```bash
$ coverage report
```

You can also generate a detailed html report in a directory named htmlcov with the following comand

```bash
$ coverage html
```

# Troubleshooting

## Views 404ing

If your newly created views are returning 404 ensure that they are added to the list in main.py.

```python
from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list
views = [
    user_views,
    index_views
]
```

## Cannot Update Workflow file

If you are running into errors in gitpod when updateding your github actions file, ensure your [github permissions](https://gitpod.io/integrations) in gitpod has workflow enabled ![perms](./images/gitperms.png)

## Database Issues

If you are adding models you may need to migrate the database with the commands given in the previous database migration section. Alternateively you can delete you database file.
