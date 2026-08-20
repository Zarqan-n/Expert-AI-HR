FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

COPY ResumeAnalyser/requirements.txt /app/ResumeAnalyser/requirements.txt
RUN pip install --no-cache-dir -r /app/ResumeAnalyser/requirements.txt

COPY . /app
WORKDIR /app/ResumeAnalyser

RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && mkdir -p /app/ResumeAnalyser/staticfiles \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:${PORT:-8000} --workers ${WEB_CONCURRENCY:-3} --access-logfile - --error-logfile - ResumeAnalyser.wsgi:application"]
