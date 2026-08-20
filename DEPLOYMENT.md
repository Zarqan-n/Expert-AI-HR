# Production deployment

This app is packaged as a container and serves Django through Gunicorn. It is stateless: resume files are processed in memory, and the app does not require a database or persistent volume.

## Render deployment

The repository includes `render.yaml`, so the simplest setup is:

1. Push the repository to GitHub or GitLab.
2. In Render, choose **New > Blueprint** and connect the repository.
3. Select the repository root where `Dockerfile` and `render.yaml` are located.
4. Review the `experthr` web service and click **Apply**.
5. Enter the secret values for `GROQ` and `MODEL` when Render prompts for them.

Render will build the root `Dockerfile`, expose port `8000`, and check `/health/`.

### Manual Render settings

If you create a Web Service instead of using the Blueprint, use these values:

| Setting | Value |
| --- | --- |
| Runtime | Docker |
| Root Directory | Leave blank, or use the repository root `.` |
| Dockerfile Path | `./Dockerfile` |
| Docker Context | `.` |
| Health Check Path | `/health/` |
| Build Command | Leave blank |
| Start Command | Leave blank |

The Dockerfile already runs `collectstatic` and starts Gunicorn. Do not add a migration command because this app has no database.

## Render environment variables

Add these under the service's **Environment** tab:

| Key | Value |
| --- | --- |
| `DEBUG` | `False` |
| `SECRET_KEY` | A long random value, or let the Blueprint generate it |
| `ALLOWED_HOSTS` | `experthr.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://experthr.onrender.com` |
| `GROQ` | Your Groq API key, stored as a secret |
| `MODEL` | The Groq model name used by your account |
| `WEB_CONCURRENCY` | `2` |

If you change the Render service name, replace `experthr.onrender.com` in both `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` with the actual `your-service.onrender.com` hostname. Add your custom domain to both values as well.

The root `.env.example` contains the same variable names for local testing. Never commit `.env` or an API key.

## Local container deployment

Build from the repository root:

```text
docker build -t experthr .
docker run --rm -p 8000:8000 --env-file .env experthr
```

The container collects static files before starting Gunicorn. Configure the platform health check to request `/health/`.

## Required production settings

Set `DEBUG=False`, a unique `SECRET_KEY`, the public hostname in `ALLOWED_HOSTS`, the HTTPS origin in `CSRF_TRUSTED_ORIGINS`, and the provider credentials used by the resume analysis code. Do not commit `.env` or database files.

## Pre-release checks

```text
cd ResumeAnalyser
..\venv\Scripts\python.exe manage.py check --deploy
..\venv\Scripts\python.exe manage.py collectstatic --noinput
```
