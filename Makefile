run:
	poetry run python .
publish: update
	poetry build
	poetry publish
update:
	poetry update
	poetry export -f requirements.txt --output requirements.txt
