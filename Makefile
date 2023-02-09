formatting:
	black --exclude venv/ .
	flake8 --ignore W503,E501 --exclude venv/ *.py sources/*.py

deploy:
	gcloud app deploy