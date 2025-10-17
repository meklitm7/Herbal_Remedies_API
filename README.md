# 🌿 Herbal Remedies API

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-darkgreen?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-API-red?logo=django&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

Robust RESTful API for managing natural herbal remedies, built with Django and Django REST Framework (DRF). Supports image uploads, search, ordering, and token-based authentication.

---

### Table of contents
- Overview
- Features
- Tech stack
- Project structure
- Getting started
- Configuration
- API reference
- Data model
- Validation rules
- Development & testing
- Deployment notes
- License

---

## Overview
The Herbal Remedies API allows users to create, browse, update, and delete herbal entries that capture common uses, ailments treated, and precautions. Read operations are public; write operations require authentication.

## Features
- CRUD for herbs with image upload support
- Token auth plus session auth for the browsable API
- Search by name, category, and uses; filter by multiple ailments
- Ordering support (e.g., by name)
- Sensible validations and unique constraints per user

## Tech stack
- Backend: Django, Django REST Framework
- Auth: DRF TokenAuth, SessionAuth (browsable API)
- Database: SQLite (dev by default), production-ready for MySQL/PostgreSQL
- Media: Local `media/` folder (served in development)

## Project structure
```
.
├─ manage.py
├─ api/                # App with models, serializers, views, urls
├─ herbal_remedies_api/
│  ├─ settings.py      # Active settings module (DJANGO_SETTINGS_MODULE=herbal_remedies_api.settings)
│  └─ requirements.txt # Python dependencies
└─ media/herb_images/  # Uploaded images (dev)
```

## Getting started
Prerequisites: Python 3.10+ and pip.

```bash
# 1) Clone
git clone https://github.com/meklitm7/herbal-remedies-api.git
cd herbal-remedies-api

# 2) Create & activate virtualenv
python -m venv .venv
source .venv/bin/activate

# 3) Install dependencies
pip install --upgrade pip
pip install -r herbal_remedies_api/requirements.txt

# 4) Apply migrations and create a superuser
python manage.py migrate
python manage.py createsuperuser

# 5) Run the dev server
python manage.py runserver

# App is now available at:
# http://127.0.0.1:8000/
```

## Configuration
Key settings live in `herbal_remedies_api/settings.py`.

- DEBUG: enabled by default for development
- ALLOWED_HOSTS: set appropriately for production
- MEDIA: served from `/media/` in development
- REST_FRAMEWORK auth defaults: Token and Session auth

Environment variables are not required for local development. For production, configure database credentials, `ALLOWED_HOSTS`, and secrets as needed.

## API reference
Base URL (local): `http://127.0.0.1:8000/`

Authentication
- Obtain token: `POST /api/token-auth/` with `username` and `password`
- Use the token in requests: `Authorization: Token 63d13d9c92c0bdcb09a167b974f5e319f8882322`
- Read endpoints are public; write endpoints require a token

### Herbs

List herbs
```
GET /api/herbs/
Query params:
  - search: string (matches name, category, uses)
  - ailment: may repeat (e.g., ?ailment=headache&ailment=fever)
  - ordering: e.g., name or -name
```

Example
```bash
curl -s "http://127.0.0.1:8000/api/herbs/?search=ginger&ordering=name"
```

Retrieve a herb
```
GET /api/herbs/{id}/
```

Create a herb (requires auth)
```bash
curl -X POST http://127.0.0.1:8000/api/herbs/ \
  -H "Authorization: Token <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ginger",
    "category": "root",
    "description": "Spicy root with broad culinary and medicinal uses.",
    "uses": "Aids digestion; anti-inflammatory",
    "ailments": "nausea, cold",
    "precautions": "May interact with blood thinners"
  }'
```

Create with image upload (multipart)
```bash
curl -X POST http://127.0.0.1:8000/api/herbs/ \
  -H "Authorization: Token <TOKEN>" \
  -F "name=Chamomile" \
  -F "category=flower" \
  -F "description=Calming herb often used in teas" \
  -F "uses=Sleep aid; mild sedative" \
  -F "ailments=insomnia, anxiety" \
  -F "image=@/absolute/path/to/photo.jpg"
```

Update a herb (PUT replaces; PATCH partial)
```bash
curl -X PATCH http://127.0.0.1:8000/api/herbs/1/ \
  -H "Authorization: Token <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"uses": "Aids digestion; anti-inflammatory; anti-nausea"}'
```

Delete a herb
```bash
curl -X DELETE http://127.0.0.1:8000/api/herbs/1/ \
  -H "Authorization: Token <TOKEN>"
```

Authentication (token)
```bash
# Obtain a token
curl -X POST http://127.0.0.1:8000/api/token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "meklit", "password": "herb7"}'

# Use in subsequent requests
# Authorization: Token <token_here>
```

Response shape (example)
```json
{
  "id": 7,
  "name": "Ginger",
  "category": "root",
  "other_category_explanation": null,
  "description": "Spicy root with broad culinary and medicinal uses.",
  "uses": "Aids digestion; anti-inflammatory",
  "ailments": "nausea, cold",
  "precautions": "May interact with blood thinners",
  "image": null,
  "image_url": null,
  "created_by": 1
}
```

## Data model
`Herb` fields
- `name` (str, required)
- `category` (choice: leaf, root, seed, flower, bark, fruit, stem, other)
- `other_category_explanation` (str, required only when `category` = `other`)
- `description` (str, required)
- `uses` (str, required)
- `ailments` (str, optional, comma-separated)
- `precautions` (str, optional)
- `image` (file, optional, uploaded to `media/herb_images/`)
- `created_by` (FK to User, set automatically on create)

## Validation rules
- Unique per user: combination of (`name`, `uses`, `created_by`) must be unique
- When `category = other`, `other_category_explanation` is required
- When `category ≠ other`, `other_category_explanation` must be empty

## Development & testing
- Admin site: `/admin/` (use your superuser)
- Browsable API login: `/api-auth/login/`
- Run tests: `python manage.py test`

Media files are served in development at `/media/`. Ensure your requests include the `request` context so `image_url` is fully qualified (done automatically in the provided views).

### ⚠️ Notes on security & deployment

- `DEBUG=True` and the dev `SECRET_KEY` are for local development only. Configure environment variables and proper hosts in production. Serve media from object storage or a CDN in production.

## License
This project is licensed under the MIT License. If distributing, include a `LICENSE` file with the full text of the MIT license.
