# online-shop







commands for running with PostgreSQL and docker-compose:

  docker-compose up

  docker-compose exec django_project python3 manage.py migrate

  docker-compose exec django_project python3 manage.py loaddata fixtures/fixture.json --app shop
