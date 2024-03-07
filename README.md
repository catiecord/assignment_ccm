# Project Name : Costumer Contact Manager

## Description
This application was created by me for as part of the coursework for the 'Software Engineering and Agile' module. It was developed in Django and MySQL and utilises several libraries such as Bootstrap and Django Rest Framework.

It is designed to be a simple contact manager for the rejected payments team at the Department of Work and Pensions. This team handles any payments that have been rejected by the bank and need to be manually processed by contacting citizens to request updated contact details or give further instructions on how to proceed. 
The team needs to be able to keep track of the contacts they have made with customers and the outcome of those contacts. 

The application incorporates user login and registration and functionally as well as different actions to different types of users.


## Installation

Source code :
    [https://github.com/catiecord/assignment_ccm](https://github.com/catiecord/assignment_ccm)

Working demonstration:


1. Clone the repository
2. Create a virtual environment and activate it
3. Install the required libraries
   - Django
   - MySQL
4. Set up the database (or use the included MySQL database) and create a new super user
    - Update settings.py with the database details
    - Run `python manage.py makemigrations` and `python manage.py migrate`
    - Run `python manage.py createsuperuser` and follow the prompts
    - Run `python manage.py loaddata initial_data.json` to load the initial data
    - Run `python manage.py runserver` to start the server
5. Run the server
    - `python manage.py runserver`
6. Navigate to the admin page and log in with the super user credentials

## Usage
The application is designed to be simple and intuitive to use. The user can navigate to the different pages using the navigation bar at the top of the page. 
The user can add a new contact, view all contacts, view a single contact, update a contact, search for a contact and log out. 
The admin user has additional functionality to delete a contact, view all users, search for a contact, activate and deactivate user accounts and access audit logs for each contact.

### Regular users can :
- Add a new contact
- View all contacts
- View a single contact
- Update a contact
- Search for a contact

### Admin users can:
- Add a new contact
- View all contacts
- View a single contact
- Update a contact
- Delete a contact
- View all users
- Search for a contact
- Activate and deactivate user accounts
- Access audit logs for each contact
  - Date and time of creation or update
  - User who created or updated the contact

# Models
The application has one model, Contact, which has the following fields:
    - created_at
    - created_by
    - payment_reference
    - first_name
    - last_name
    - contact_method
    - contact_date
    - contact_status
    - notes
    - updated_by
    - updated_at

The model is used to store the details of each contact made with a customer. The created_at and created_by fields are automatically populated when a new contact is created. The updated_by and updated_at fields are automatically populated when a contact is updated.

# Testing

The application has been tested using the Django test framework. The tests are located in the tests directory and test forms, models, urls and views.

To run the tests, navigate to the root directory and run `python manage.py test`




