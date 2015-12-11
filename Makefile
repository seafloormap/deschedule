.PHONY: requirements upgrade db

requirements: requirements.txt
	python -m venv flask
	flask/bin/pip install --requirement requirements.txt

upgrade: requirements
	flask/bin/pip install --upgrade --requirement requirements.txt

db: app/models.py
	./db_create.py

app.db: db
