formatting:
	black .
	flake8 --ignore W503,E501 --exclude venv/ *.py

deploy:
	gcloud app deploy