web: gunicorn consignment.wsgi --log-file -
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
