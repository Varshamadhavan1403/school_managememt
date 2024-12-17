## Project Description
This is a Django-based project that implements **Role-Based Access Control (RBAC)** using Django's built-in `Groups` and `Permissions` features. It includes roles such as `Admin`, `Office Staff`, and `Librarian`, with each role having specific access privileges.

### Features
- Admin can manage (create, edit, delete) Office Staff and Librarian accounts.
- Office Staff can view and edit student details.
- Librarians can view student and library records.
- Role-based access control using Django `Permissions` and `Groups`.

---

## Setup Instructions

### Prerequisites
- Python 3.8 or later
- Django 4.0 or later
- A virtual environment tool like `venv` or `virtualenv`

### Steps to Set Up
1. Clone the repository:
   ```bash
   git clone https://github.com/Varshamadhavan1403/school_managememt.git
   cd django-rbac-project
2. Create a virtual environment
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
3. Install required libraries
    pip install -r requirements.txt
4. Set up the .env file (if needed):
    Create a .env file in the root directory and add the following:
    
    SECRET_KEY=your-secret-key
    DEBUG=True
    ALLOWED_HOSTS=localhost, 127.0.0.1
5. Run migrations
    python manage.py makemigrations
    python manage.py migrate
6. Create a superuser
    python manage.py createsuperuser
7. Start development server
    python manage.py runserver
8. Access the application at:
    Admin Panel: http://127.0.0.1:8000/admin
    API Endpoints: http://127.0.0.1:8000/usersapp/
                    http://127.0.0.1:8000/student/
                    http://127.0.0.1:8000/libraryapp/
                    http://127.0.0.1:8000/feeapp/

### Environment Variables

1. SECRET_KEY: The secret key for Django.
2. DEBUG: Set to True for development; False for production.
3. ALLOWED_HOSTS: Hosts allowed to access the application.

### Libraries Used
Below is a list of libraries used in this project:
1. Django: Python web framework
    pip install django
2. djangorestframework: For building APIs
    pip install djangorestframework
3. python-decouple: For managing environment variables
    pip install python-decouple
4. djangorestframework-simplejwt: For JWT-based authentication
    pip install djangorestframework-simplejwt
5. django-environ (Optional): For environment variable management
    pip install django-environ

