# Django Blog

A full-stack blog application built with **Django** and **Bootstrap**.

The project includes user authentication, profiles, blog posts, image uploads, comments, likes/dislikes, search, pagination, and post management.

## Features

- User signup and login
- Logout
- User profile
- Profile picture upload
- Update profile information
- Create blog posts
- Upload post images
- Publish/unpublish posts
- Edit and soft-delete your own posts
- View all published posts
- Search posts by title or content
- Pagination
- Post detail pages
- Comments
- Edit and delete your own comments
- Like/dislike reactions
- Prevent multiple reactions from the same user on the same post
- Password reset/change pages
- Django admin support
- Responsive Bootstrap-based UI

## Tech Stack

- Python
- Django
- SQLite
- HTML
- CSS
- Bootstrap

## Project Structure

```text
django_blog/
├── blog/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── django_blog/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── static/
│   ├── css/
│   └── icons/
├── templates/
├── media/                 # Local uploaded files; not committed to Git
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10+ recommended
- pip
- Git

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY/django_blog
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv myenv
myenv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and set your secret key.

For Windows Command Prompt:

```bash
copy .env.example .env
```

For PowerShell:

```powershell
Copy-Item .env.example .env
```

For macOS/Linux:

```bash
cp .env.example .env
```

> Never commit your real `.env` file.


### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create an admin user

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```

## Database

The project uses SQLite for local development.

The database file is intentionally excluded from Git. When another developer clones the project, they can create a fresh database by running:

```bash
python manage.py migrate
```

## Media Uploads

User-uploaded files are stored locally under:

```text
media/
```

This includes:

- post images
- profile pictures

The `media/` directory is excluded from Git because uploaded files are user-specific and can become large.

## Static Files

Static files are stored under:

```text
static/
```

The project currently contains custom CSS and reaction/search icons.

## Development Notes

This project is configured for local development. Before deploying to production, review:

- `DEBUG`
- `SECRET_KEY`
- `ALLOWED_HOSTS`
- database configuration
- static file handling
- media storage
- HTTPS/security settings
- email configuration

## Future Improvements

Possible next features:

- Django Forms
- Class-based views
- User profile pages for other users
- Follow system
- Categories and tags
- Rich text editor
- Comment pagination
- AJAX reactions/comments
- REST API with Django REST Framework
- Email verification
- Password reset through email
- Production deployment
- PostgreSQL
- Cloud media storage
- Automated tests
- CI/CD

## Author

**Sumanta Sahoo**

B.Tech Graduate | Python | Django | Java | HTML | CSS

---

If you find this project useful, feel free to ⭐ the repository.
