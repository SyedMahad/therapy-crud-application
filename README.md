# Therapy CRUD Application

This is a Django-based web application that provides a CRUD (Create, Read, Update, Delete) interface for managing therapy appointments between patients and counselors.

## System Requirements

![Python](https://img.shields.io/badge/python-3.8.16-blue.svg)  
![Django](https://img.shields.io/badge/django-3.2.18-green.svg)  
![Django Rest Framework](https://img.shields.io/badge/django--rest--framework-3.14.0-red.svg)  
[![djangorestframework-simplejwt v5.2.2](https://img.shields.io/badge/djangorestframework--simplejwt-5.2.2-blue)](https://pypi.org/project/djangorestframework-simplejwt/5.2.2/)  
[![django-filter v23.1](https://img.shields.io/badge/django--filter-23.1-blue)](https://pypi.org/project/django-filter/23.1/)  

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/SyedMahad/therapy-crud-application.git
    ```
1. Create a virtual environment (optional):
    ```sh
    python -m venv env
    ```
1. Activate the virtual environment (optional):
    ```sh
    Windows: env\Scripts\activate
    Unix or Linux: source env/bin/activate
    ```
1. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```
1. Migrate the database:
    ```sh
    python manage.py migrate
    ```

## Running the Application

1. Activate the virtual environment (if created):
    ```sh
    Windows: env\Scripts\activate
    Unix or Linux: source env/bin/activate
    ```
1. Start the development server:
    ```sh
    python manage.py runserver
    ```
1. Access the application in a web browser at
    ```sh
    http://localhost:8000
    ```

## Additional Information

- The application uses some third-party APIs, which are included in the requirements.txt file.
- Environment variables are not required for running the application.