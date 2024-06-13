# Lunch_decision

## Description
This Django project implements a menu management system where users can create restaurants, upload daily menus, vote for menus, and manage users.

### Steps to Run the Project

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ArtemKrayevskiy/Lunch_decision.git
   cd lunch_decision

2. **Start the containers**
   ```bash
   $ docker-compose up -d --build
   
3. **Do the migrations**
   ```bash
   $ docker-compose run web python manage.py makemigrations
   $ docker-compose run web python manage.py migrate

4. **After that you may try to start the server**
   ```bash
   $ python3 manage.py runserver

5. **Run Tests**
   ```bash
   $ pytest

   
