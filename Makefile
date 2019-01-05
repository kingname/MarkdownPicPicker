init:
	pip install pipenv --upgrade
	pipenv lock
	pipenv install --dev
test:
	pipenv run python test.py
