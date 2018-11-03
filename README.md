# contact_box
Contact box application written in Django

## Run project
#### PostgresSQL
The app is configured to work with PostgresSQL database and it's required to set the following environmental variables:
* DJANGO_SECRET_KEY
* DATABASE_NAME
* DATABASE_USER
* DATABASE_PASSWORD
* DATABASE_HOST
* EMAIL_USER
* EMAIL_PASS

You can take this code, put it in your text editor, fill values and paste to terminal

```
export DJANGO_SECRET_KEY='<fill>'
export DATABASE_NAME='<fill>'
export DATABASE_USER='<fill>'
export DATABASE_PASSWORD='<fill>'
export DATABASE_HOST='<fill>'
export EMAIL_USER='<fill>'
export EMAIL_PASS='<fill>'
```

#### SQLite3

You can use SQLite3 as well. Default settings are commented-out. Just uncomment them and delete/comment previous database settings.
WARNING! You still have to set environmental variable for DJANGO_SECRET_KEY.

#### Dependencies

```bash
$ cd src
$ pip install -r requirements.txt
```

## Project details
#### Database visualisation

![alt text](/img/contact_box_visualized.png)

#### Django lessons learned
* User authentication
* Generic views and mixins
* Custom model managers and querysets
* Forms, formsets, inline formsets
* Custom template filters
* Pagination
* Crispy forms
* Django debug toolbar
* Email backend (password recovery)
* Graph models ([pygraphviz](https://django-extensions.readthedocs.io/en/latest/graph_models.html))
* Signals

#### Other lessons learned
* Responsive Web Design (Bootstrap)
* Heroku deployment
