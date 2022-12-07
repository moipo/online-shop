# online-shop

use the following commands to run this project properly with Docker and PostgreSQL (fixtures required):

docker-compose up

docker-compose exec django_project python3 manage.py migrate

docker-compose exec django_project python3 manage.py loaddata fixtures/fixture.json --app shop
