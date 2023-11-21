#!/bin/sh
echo "Works well"
python manage.py migrate
echo "import os; from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(os.getenv('ADMIN_USERNAME'), os.getenv('ADMIN_EMAIL'), os.getenv('ADMIN_PASSWORD'), os.getenv('ADMIN_EMAIL'), os.getenv('ADMIN_PASSWORD'))" | python manage.py shell
python manage.py runserver 0.0.0.0:8000
$@
