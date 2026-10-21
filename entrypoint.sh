#!/bin/sh
set -e

if [ "$DATABASE_URL" ]; then
    echo "Waiting for PostgreSQL database..."
    
    while ! python -c "
import sys, os, dj_database_url, psycopg
try:
    url = os.environ.get('DATABASE_URL')
    if url and url.startswith('postgres'):
        cfg = dj_database_url.parse(url)
        conn = psycopg.connect(
            dbname=cfg['NAME'],
            user=cfg['USER'],
            password=cfg['PASSWORD'],
            host=cfg['HOST'],
            port=cfg['PORT'] or 5432,
            connect_timeout=3
        )
        conn.close()
    sys.exit(0)
except Exception as e:
    sys.exit(1)
"; do
        echo "PostgreSQL is unavailable - sleeping 1s"
        sleep 1
    done

    echo "PostgreSQL is ready!"
fi

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Seeding breakfast recipes from Eric Adjepong's Ghana to the World..."
python manage.py seed_recipes || true

echo "Collecting static files for WhiteNoise..."
python manage.py collectstatic --noinput

echo "Ensuring superuser exists..."
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easybreakfast.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin1234')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created.')
else:
    print(f'Superuser {username} already exists.')
" || true

echo "Starting Django server..."
exec "$@"
