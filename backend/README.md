Step 1: Initialize the Project and Apps
Open your VS Code terminal (ensuring campus_env is activated) and run these commands to create the core structure:

```bash
conda activate campus_env
# Create the main Django project (the dot creates it in the current directory)
django-admin startproject campus_platform .

# Create our two core apps
python manage.py startapp users
python manage.py startapp resources
```

Step 4: Apply Migrations
Once you have created the database campus_db in Laragon, run these commands to push your schema to MySQL:


```bash
python manage.py makemigrations users
python manage.py makemigrations resources
python manage.py migrate
```

Think of Django migrations as version control for your database schema.
Just as Git tracks changes to your code, migrations track changes to your database structure (tables, columns, and relationships). Instead of writing raw SQL like ALTER TABLE or CREATE TABLE, you modify your Python models, and Django handles the database updates for you.


```bash
$ python manage.py createsuperuser
```

username: meitong
password: meitong
email: blank


```bash
pip install djangorestframework djangorestframework-simplejwt
```


Could use VS Code Postman to test api.