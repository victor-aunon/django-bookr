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