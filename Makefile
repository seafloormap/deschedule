.PHONY: upgrade

requirements: requirements.txt
	python -m venv flask
	flask/bin/pip install --requirement requirements.txt

upgrade: requirements
	flask/bin/pip install --upgrade --requirement requirements.txt
