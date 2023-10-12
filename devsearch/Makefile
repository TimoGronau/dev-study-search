start:
	python manage.py runserver
install:
	pip install -r requirements/dev.txt
migrate:
	python manage.py migrate 
migrations:
	python manage.py makemigrations 
showmigrations:
	python manage.py showmigrations 
sqlmigrate:
	python manage.py sqlmigrate $(App) $(Migration) 
shell:
	python manage.py shell 
rollback:
	python manage.py migrate $(a) $(m) 
test:
	python manage.py test 
collectstatic:
	python manage.py collectstatic