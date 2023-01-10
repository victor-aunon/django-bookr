1. Install django with `pip install django`
2. Initialize the project with `django-admin startproject <name>`
3. Initialize the server with `py <name>\manage.py runserver`
4. Create a Django app with `py <name>\manage.py startapp <app-name>`
5. Creating a MVT:
  - Create a data model in `<app-name>\models.py`
  - Create an endpoint as a function in `<app-name>\views.py`
  - Create a template as an HTML file in `<app-name>\templates\<template>.html`
6. Create new DB migrations with `py <name>\manage.py makemigrations <app-name>`
7. Perform DB migrations with `py <name>\manage.py migrate`
8. Using custom commands:
  - Create a python file within `<app-name>\management\commands`
  - Include a class *Command* that extends *BaseCommand*
  - Include the logic of the command in a class method called *handle*
  - Run the custom command with `py <name>\manage.py <command> <args>`
9. Create a superuser with `py <name>\manage.py createsuperuser`
10. Register models on admin site by including `admin.site.register(<model>)` in `<app-name>\admin.py` file
11. Serve static files using the `{% load static %}` instruction at the beginning of the template file
12. Set static files directory in `<name>\settings.py` by including:
```
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
```
13. Invalidate caches (hash file names) with the setting:
```
 STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
```
14. Add `{% csrf_token %}` to a form template that uses a POST method to avoid CSRF attacks
15. Create form classes by extending *ModelForm* to build a form from a model
16. Store uploaded files in `MEDIA_ROOT`. Serve media from `MEDIA_URL`
17. Install **djangorestframework** to create a Django API
18. Add `rest_framework`to `INSTALLED_APPS` in `<name>\settings.py` file
19. Create the serializers for each model
20. Write endpoints in the `api_views.py` file