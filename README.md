### 🌿 Herbal Remedies API

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-darkgreen?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-API-red?logo=django&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

### 📌 What this project is

The Herbal Remedies API is a Django + Django REST Framework (DRF) backend that lets you create, read, update, and delete records describing medicinal herbs, their uses, precautions, and optional images. It exposes clean REST endpoints secured with token or session auth. Anonymous users can browse; write operations require authentication.

---

### 🧠 How it works (high-level)

- The `api` app defines a `Herb` model and the REST API.
- DRF generic views (`ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`) provide CRUD.
- Permissions: `IsAuthenticatedOrReadOnly` means GET is public; POST/PUT/PATCH/DELETE require login.
- Image uploads use `ImageField` saved to `media/herb_images/`; `image_url` is computed per request.
- Search across `name`, `category`, `uses`; filter by one or more `ailment` query params.

Request flow:
1) Client calls `/api/herbs/` or `/api/herbs/{id}/`.
2) DRF view validates data with `HerbSerializer` and enforces rules.
3) On create/update, `created_by` is set from the authenticated user.
4) Responses are JSON, including absolute `image_url` when an image exists.

---

### 🗂️ Project structure (relevant parts)

```
.
├── manage.py
├── herbal_remedies_api/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── api/
    ├── models.py
    ├── serializers.py
    ├── views.py
    └── urls.py
```

Note: You may see nested duplicate Django project folders in `herbal_remedies_api/`. Use the root-level `manage.py` and `herbal_remedies_api/settings.py` shown above.

---

### 🧱 Data model

`Herb` fields:
- `name` (str, required)
- `category` (choice: `leaf`, `root`, `seed`, `flower`, `bark`, `fruit`, `stem`, `other`)
- `other_category_explanation` (str, required only when `category=other`; forbidden otherwise)
- `description` (str, required)
- `uses` (str, required) — general medicinal uses
- `ailments` (str, optional) — comma-separated ailments, e.g. "headache, fever"
- `precautions` (str, optional)
- `image` (file, optional) — stored in `media/herb_images/`
- `created_by` (User FK, read-only; set by server)

Uniqueness: A user cannot create two herbs with the same `name` and `uses` pair (`unique_together = (name, uses, created_by)`).

---

### 🔐 Authentication & permissions

- Default: `IsAuthenticatedOrReadOnly` — anyone can GET; only authenticated users can modify.
- Token auth endpoint: `POST /api/token-auth/` returns a DRF token for a username/password.
- Session auth for the browsable API: login at `/api-auth/login/`.

Send the token on write requests:

```http
Authorization: Token YOUR_TOKEN_HERE
```

---

### 🔎 Querying, search, and filtering

- Search by name, category, uses: `GET /api/herbs/?search=ginger`
- Filter by ailments (repeatable): `GET /api/herbs/?ailment=headache&ailment=fever`

---

### 🌐 REST API endpoints

- `POST /api/token-auth/` — exchange username/password for a token
- `GET /api/herbs/` — list herbs (public)
- `POST /api/herbs/` — create herb (auth required)
- `GET /api/herbs/{id}/` — retrieve single herb (public)
- `PUT|PATCH /api/herbs/{id}/` — update herb (auth required)
- `DELETE /api/herbs/{id}/` — delete herb (auth required)

Response shape (example):

```json
{
  "id": 3,
  "name": "Ginger",
  "category": "root",
  "other_category_explanation": null,
  "description": "A warming root used for digestion.",
  "uses": "Nausea relief; digestion support",
  "ailments": "nausea, motion sickness",
  "precautions": "Consult your doctor if on blood thinners.",
  "image": "herb_images/1800ss_getty_rf_ginger.webp",
  "image_url": "http://localhost:8000/media/herb_images/1800ss_getty_rf_ginger.webp",
  "created_by": 1
}
```

Validation rules enforced by the API:
- `category=other` requires `other_category_explanation`.
- Standard categories forbid `other_category_explanation`.
- Duplicate (`name`, `uses`) for the same user is rejected.

---

### 📤 Creating & updating herbs (content types)

These endpoints accept `multipart/form-data` or `application/x-www-form-urlencoded` (JSON is not enabled on create/update by default). Prefer multipart so you can include an optional image.

Create without image:

```bash
curl -X POST http://localhost:8000/api/herbs/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "name=Ginger" \
  --data-urlencode "category=root" \
  --data-urlencode "description=A warming root used for digestion." \
  --data-urlencode "uses=Nausea relief; digestion support" \
  --data-urlencode "ailments=nausea, motion sickness" \
  --data-urlencode "precautions=Consult your doctor if on blood thinners."
```

Create with image:

```bash
curl -X POST http://localhost:8000/api/herbs/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "name=Ginger" \
  -F "category=root" \
  -F "description=A warming root used for digestion." \
  -F "uses=Nausea relief; digestion support" \
  -F "ailments=nausea, motion sickness" \
  -F "image=@/path/to/ginger.jpg"
```

Partial update (PATCH):

```bash
curl -X PATCH http://localhost:8000/api/herbs/3/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "precautions=Avoid high doses during pregnancy"
```

Search and filter example:

```bash
curl "http://localhost:8000/api/herbs/?search=root&ailment=nausea&ailment=fever"
```

---

### ⚙️ Setup & local development

Prereqs: Python 3.10+ and pip.

1) Clone and enter the project

```bash
git clone https://github.com/meklitm7/herbal-remedies-api.git
cd herbal-remedies-api
```

2) Create a virtual environment and install deps

```bash
python -m venv .venv
source .venv/bin/activate
pip install "Django>=5.2.5" djangorestframework djangorestframework-authtoken Pillow
```

3) Apply migrations and create a superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

4) Run the server

```bash
python manage.py runserver
```

5) Get a token and call the API

```bash
curl -X POST http://localhost:8000/api/token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "youruser", "password": "yourpass"}'

curl http://localhost:8000/api/herbs/ \
  -H "Authorization: Token YOUR_TOKEN"
```

Media files are served at `/media/` in development (configured via `MEDIA_URL`/`MEDIA_ROOT`).

---

### 🧭 Browsable API

Open `http://localhost:8000/api/herbs/` in a browser. Log in via the top-right link (`/api-auth/login/`) to try write operations.

---

### 🧪 Testing

The project currently includes an empty `api/tests.py`. You can add DRF API tests with `APITestCase`.

---

### 🔧 Troubleshooting

- 401 Unauthorized: Add `Authorization: Token …` header or log in via session.
- 400 Bad Request: Check validation rules (category/explanation, duplicate `name` + `uses`).
- 415 Unsupported Media Type: Use form-data or x-www-form-urlencoded for create/update.
- Image not showing: ensure Pillow is installed and you are in DEBUG/development so media is served.

---

### 🗺️ Roadmap

- Pagination and ordering across fields
- Rich search/filter UX
- JWT auth (optional) or extend token flow
- Collections/favorites and user-specific views

---

### ⚠️ Notes on security & deployment

- `DEBUG=True` and the dev `SECRET_KEY` are for local development only. Configure environment variables and proper hosts in production. Serve media from object storage or a CDN in production.

---

### 📄 License

MIT
