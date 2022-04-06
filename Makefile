setup:
	poetry install
	poetry run pre-commit install

run:
	poetry run python entry.py --run

revision:
	poetry run python entry.py --revision

migrate:
	poetry run python entry.py --migrate

lint:
	black entry.py bot
	isort entry.py bot/ --profile=black
