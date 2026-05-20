# Change this line to python3 for Mac compatibility
GLOBAL_PYTHON = python3

PYTHON = ./venv/bin/python
PIP = ./venv/bin/pip
.DEFAULT_GOAL := all

all:
	$(GLOBAL_PYTHON) -m venv venv
	$(PIP) install -r requirements.txt
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate
	$(PYTHON) manage.py seed_categories
	$(PYTHON) manage.py seed_data
	$(PYTHON) manage.py runserver
