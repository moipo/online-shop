# online-shop

Shop of electronics, that gets info about the current exchange rate and shows it via a backend websocket. It also includes multiple product filters, authentication, pagination and much more.   




Run the project in a container:

    docker build -t online_shop_img .
  
    docker run -d -p 8000:8000 online_shop_img



Commands for running with a PostgreSQL and docker-compose:

    docker-compose up
  
    docker-compose exec django_project python3 manage.py migrate
  
    docker-compose exec django_project python3 manage.py loaddata fixtures/fixture.json --app shop



You can also run tests:

    python manage.py test shop/tests
