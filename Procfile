release: cp -fv example.env .env && cd api && python manage.py makemigrations && python manage.py migrate
web: cd api && python manage.py runserver 0.0.0.0:$PORT
