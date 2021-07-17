start:
	python manage.py runserver localhost:4243 -v 3 --settings=settings.dev

mm:
	python manage.py migrate --settings=settings.dev

test:
	python manage.py test --settings=settings.dev -v 2

shell:
	python manage.py shell

coverage:
	coverage run --source='.' manage.py test --settings=settings.dev
	coverage report -m

up:
	sudo docker-compose up --force-recreate --build

clear:
	sudo docker context use default
	sudo docker system prune -a

worker:
	celery -A app.core worker -l info
