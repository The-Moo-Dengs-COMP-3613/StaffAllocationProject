[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/uwidcit/flaskmvc)
<a href="https://render.com/deploy?repo=https://github.com/uwidcit/flaskmvc">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>

![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)



# Flask Commands

The database is initialized with mock data. Before executing the commands for the project requirements, initialize the database by executing the following command:

```bash
$ flask init
```


## Mock Data

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



Requirement #2 - creating a staff member (lecturer, tutor or TA):

```python
# inside wsgi.py

staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("create", help="Creates a staff member")
@click.argument("title")
@click.argument("first_name")
@click.argument("last_name")
@click.argument("role")
def create_staff_command(title, first_name, last_name, role):
    staff = create_staff(title, first_name, last_name, role)
    print(f'Staff member {staff.firstName} {staff.lastName} created!')

app.cli.add_command(staff_cli)



```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash
$ flask staff create "title" "first name" "last name" "role (lecturer, tutor or TA)"
```

For example: 

```bash
$ flask staff create Dr Heinz Doofenshmirtz lecturer
```



Requirement #3 - assigning a staff member to a course

```python
# inside wsgi.py

@course_cli.command("assign", help="Assign staff to a course")
@click.argument("course_code")
@click.argument("lecturer_id", required=False)
@click.argument("tutor_id", required=False)
@click.argument("ta_id", required=False)
def assign_staff_command(course_code, lecturer_id=None, tutor_id=None, ta_id=None):
    success = assign_staff_to_course(course_code, lecturer_id, tutor_id, ta_id)
    if success:
        # Fetch and display staff names
        course = Course.query.filter_by(courseCode=course_code).first()
        lecturer = Staff.query.get(course.lecturer_id)
        tutor = Staff.query.get(course.tutor_id)
        ta = Staff.query.get(course.ta_id)

        lecturer_name = f"{lecturer.title} {lecturer.firstName} {lecturer.lastName}" if lecturer else "None"
        tutor_name = f"{tutor.title} {tutor.firstName} {tutor.lastName}" if tutor else "None"
        ta_name = f"{ta.title} {ta.firstName} {ta.lastName}" if ta else "None"

        print(f'Staff assigned to course {course_code} successfully!')
        print(f'Lecturer: {lecturer_name}')
        print(f'Tutor: {tutor_name}')
        print(f'Teaching Assistant: {ta_name}')
    else:
        print(f'Course {course_code} not found!')


```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash
$ flask course assign "course code" "lecturer id" "tutor id" "TA id"
```

For example: 

```bash
$ flask course assign "COMP101" 1 2 3
```



Requirement #4 - view course details

```python
# inside wsgi.py

@course_cli.command("view", help="View course details")
@click.argument("course_code")
def view_course_command(course_code):
    details = view_course_details(course_code)
    if isinstance(details, str):
        print(details)
    else:
        print("Course Details:")
        for key, value in details.items():
            print(f"{key}: {value}")

app.cli.add_command(course_cli)



```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash
$ flask course view "course code" 
```

For example: 

```bash
$ flask course view COMP101
```


