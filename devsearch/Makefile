dev-start:
	python manage.py runserver
dev-install:
	pip install -r requirements/dev.txt
dev-migrate:
	python manage.py migrate 
dev-makemigrations:
	python manage.py makemigrations 
dev-showmigrations:
	python manage.py showmigrations 
dev-sqlmigrate:
	python manage.py sqlmigrate $(App) $(Migration) 
dev-shell:
	python manage.py shell 
dev-rollback:
	python manage.py migrate $(a) $(m) 
dev-test:
	python manage.py test 