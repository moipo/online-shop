# online-shop

Ecommerce store of tech


Run the project in a container:

    docker build -t online_shop_img .
  
    docker run -d -p 8000:8000 online_shop_img



Commands for running with a PostgreSQL and docker-compose:

    docker-compose up
  
    docker-compose exec django_project python3 manage.py migrate
  
    docker-compose exec django_project python3 manage.py loaddata fixtures/fixture.json --app shop



Static analysis tools::

    black shop

    autoflake --remove-all-unused-imports -i -r shop

    isort shop

    pylint --load-plugins pylint_django --django-settings-module=online_shop.settings --ignore=migrations shop



Frontend part of the project was designed by HTMLcodex:

  =>  Template Name    : MultiShop - Online Shop Website Template

  =>  Template Link    : https://htmlcodex.com/online-shop-website-template

  =>  Template License : https://htmlcodex.com/license (or read the LICENSE.txt file)

  =>  Template Author  : HTML Codex

  =>  Author Website   : https://htmlcodex.com

  =>  About HTML Codex : HTML Codex is one of the top creators and publishers of Free HTML templates, HTML landing pages, HTML email templates and HTML snippets in the world. Read more at ( https://htmlcodex.com/about-us )