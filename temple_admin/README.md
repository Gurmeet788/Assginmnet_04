# Temple Admin Management System

A Flask + Supabase based temple website administration system built as a learning project. The project demonstrates authentication, authorization, JWT handling, REST APIs, Supabase Database, Supabase Storage, Row Level Security (RLS), and a simple HTML/CSS/JavaScript admin frontend.

## Project Goals

This project was built to practice:

- Flask REST API development
- Supabase Authentication
- JWT-based authentication
- Role-based authorization for admins
- Decorators and middleware
- CRUD operations
- PostgreSQL/Supabase database integration
- Supabase Storage for uploaded files
- Row Level Security (RLS)
- HTML/CSS/JavaScript frontend integration
- Testing APIs with Postman

## Main Features

### Authentication

- User signup
- User login
- User logout
- JWT access-token based authentication
- Protected routes using `@require_auth`
- Admin-only routes using `@require_admin`
- Reuse of an old token after logout is rejected with `401 Unauthorized` in the tested flow

### Authorization

The application distinguishes between normal users and administrators.

Protected admin routes require:

```text
Valid JWT
   +
Admin role
```

A normal authenticated user receives `403 Forbidden` when trying to access an admin-only operation.

### Announcement Management

Public endpoint:

```http
GET /api/announcement
```

Admin endpoint:

```http
PATCH /api/admin/announcement
```

The PATCH endpoint can update:

- title only
- content only
- both title and content

The announcement record uses a UUID primary key.

### Gallery Management

Public endpoint:

```http
GET /api/gallery
```

Admin endpoints:

```http
POST /api/admin/gallery
DELETE /api/admin/gallery/<gallery_id>
```

Gallery upload flow:

```text
Admin selects file
      ↓
Flask receives multipart/form-data
      ↓
File uploaded to Supabase Storage
      ↓
Public image URL generated
      ↓
URL + caption saved in gallery table
```

Gallery deletion removes both:

1. the actual object from Supabase Storage
2. the corresponding record from the `gallery` table

## Database

### `announcements`

| Column | Type | Description |
|---|---|---|
| `id` | UUID | Unique announcement identifier |
| `title` | text | Announcement title |
| `content` | text | Announcement content |
| `updated_at` | timestamptz | Last update time |

### `gallery`

| Column | Type | Description |
|---|---|---|
| `id` | UUID | Unique gallery identifier |
| `image_url` | text | Public URL of the stored file |
| `caption` | text | Optional image caption |
| `created_at` | timestamptz | Creation time |

### Supabase Storage

Bucket:

```text
gallery
```

The database stores the file URL and metadata, while the actual uploaded file is stored in Supabase Storage.

## RLS Policies

### Announcements

- Public users can read announcements.
- Authenticated administrators can update announcements.

### Gallery table

- Public users can read gallery records.
- Administrators can insert gallery records.
- Administrators can delete gallery records.

### Storage bucket

- Gallery files are publicly viewable.
- Administrators can upload gallery files.
- Administrators can delete gallery files.

## API Summary

| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| `POST` | `/auth/signup` | Public | Create user |
| `POST` | `/auth/login` | Public | Login and receive access token |
| `POST` | `/auth/logout` | Authenticated | Logout |
| `GET` | `/api/announcement` | Public | Get announcement |
| `PATCH` | `/api/admin/announcement` | Admin | Update announcement |
| `GET` | `/api/gallery` | Public | Get gallery records |
| `POST` | `/api/admin/gallery` | Admin | Upload gallery file and create record |
| `DELETE` | `/api/admin/gallery/<gallery_id>` | Admin | Delete gallery file and record |

## Frontend

The admin frontend contains:

```text
templates/
└── admin/
    ├── login.html
    ├── signup.html
    └── dashboard.html

static/
└── admin/
    └── js/
        ├── login.js
        ├── signup.js
        └── dashboard.js
```

### Frontend Flow

```text
Signup
  ↓
POST /auth/signup

Login
  ↓
POST /auth/login
  ↓
Access token
  ↓
localStorage
  ↓
Admin dashboard
```

The dashboard uses JavaScript `fetch()` to communicate with the Flask APIs.

For protected requests, the access token is sent as:

```http
Authorization: Bearer <access_token>
```

## Project Structure

A simplified structure is:

```text
Assginmnet_04/
│
├── temple_admin/
│   ├── app.py
│   ├── supabase_client.py
│   ├── .env
│   ├── requirements.txt
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── admin/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py
│   │
│   ├── content/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── templates/
│   │   └── admin/
│   │       ├── login.html
│   │       ├── signup.html
│   │       └── dashboard.html
│   │
│   └── static/
│       └── admin/
│           └── js/
│               ├── login.js
│               ├── signup.js
│               └── dashboard.js
│
└── README.md
```

## Environment Variables

Create a `.env` file in the backend directory.

Example:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_public_key
SUPABASE_SECRET_KEY=your_server_side_secret_key
```

Do not commit `.env` or secret keys to GitHub.

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask application from the `temple_admin` directory:

```bash
python app.py
```

When the application starts, Flask runs the local development server on the configured port.
In the current project configuration, the server runs on port **3000**:

```text
http://127.0.0.1:3000
```

Open the admin login page at:

```text
http://127.0.0.1:3000/admin/login
```

### Quick Start (Windows)

From the project directory:

```bash
cd temple_admin
venv\Scripts\activate
python app.py
```

Then open:

```text
http://127.0.0.1:3000/admin/login
```

To stop the development server, press `Ctrl + C` in the terminal.

## Testing

Postman was used to test the backend APIs.

Examples:

### Get announcement

```http
GET /api/announcement
```

### Update announcement

```http
PATCH /api/admin/announcement
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

Example body:

```json
{
  "id": "announcement-uuid",
  "title": "Updated title",
  "content": "Updated content"
}
```

### Get gallery

```http
GET /api/gallery
```

### Upload gallery file

```http
POST /api/admin/gallery
Authorization: Bearer <admin_access_token>
```

Use `multipart/form-data` with:

```text
image   = file
caption = text
```

### Delete gallery item

```http
DELETE /api/admin/gallery/<gallery_uuid>
Authorization: Bearer <admin_access_token>
```

## Security Notes

- JWT authentication is required for protected admin APIs.
- Admin authorization is checked separately from authentication.
- Supabase RLS policies protect the database tables.
- The server-side Supabase secret/service key must never be exposed to frontend JavaScript.
- The frontend stores the access token in browser `localStorage` for this learning project.

## Learning Outcomes

By completing this project, the main concepts practiced were:

1. HTTP methods: GET, POST, PATCH, DELETE
2. Query parameters and route parameters
3. Flask Blueprints
4. Decorators and `@wraps`
5. JWT authentication
6. Role-based authorization
7. Supabase Auth
8. Supabase PostgreSQL database operations
9. Supabase Storage
10. Row Level Security
11. JavaScript `fetch()` and asynchronous requests
12. JSON and `FormData`
13. Browser `localStorage`
14. Frontend-backend integration

## Notes

This is a learning-focused implementation. The website content is intentionally kept small: the main static pages can remain hardcoded while announcements and gallery content are managed dynamically through the admin dashboard.
